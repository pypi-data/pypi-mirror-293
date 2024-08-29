import importlib
import os
import sys
from io import BytesIO
from typing import List

import numpy as np
import pixelengine
from cachetools import LRUCache, cached
from cds_plugin_utils.base_slide_instance import BaseSlideInstance
from PIL import Image

from . import slide_utils


class IsyntaxSlideInstance(BaseSlideInstance):
    supported_vendor_formats = {
        "isyntax": [".isyntax"],
    }

    def __init__(self, filepath: str, padding_color: tuple = (255, 255, 255)):
        data_dir = os.getenv("PLUGIN_ISYNTAX_DATA_DIR") if os.getenv("PLUGIN_ISYNTAX_DATA_DIR") else "/data"
        self.pe_input = None
        self.slide_info = None
        self.pixel_engine = None

        self.abs_filepath = f"{data_dir.rstrip('/')}/{filepath.lstrip('/')}"
        self.padding_color = padding_color

        if str(self.abs_filepath).endswith(".isyntax"):
            if importlib.find_loader("pixelengine") is None:
                self.result = {
                    "rep": "error",
                    "status_code": 500,
                    "detail": f"Could not import Philips pixel engine.",
                }

            try:
                render_backend, render_context = self.__get_backends("SOFTWARE")
                self.pixel_engine = pixelengine.PixelEngine(render_backend, render_context)
                self.pe_input = self.pixel_engine["in"]
                self.pe_input.open(self.abs_filepath)

                self.image_names = []
                for index in range(self.pe_input.num_images):
                    image_type = self.pe_input[index].image_type
                    self.image_names.append(image_type)

                self.result = slide_utils.get_success_response(
                    content={
                        "is_supported": True,
                        "format": "isyntax",
                        "plugin": "isyntax",
                        "storage_addresses": [{"main_address": True, "address": filepath}],
                    }
                )
            except RuntimeError as ex:
                self.result = slide_utils.get_error_response(
                    status_code=500, detail=f"Failed to open isyntax file. [{ex}]"
                )
        else:
            self.result = slide_utils.get_success_response(
                content={
                    "is_supported": False,
                    "format": None,
                    "plugin": "isyntax",
                    "storage_addresses": [],
                }
            )

    def close(self):
        if self.pe_input:
            self.pe_input.close()

    def get_slide_info(self):
        if self.slide_info is None:
            self.slide_info = self.__get_slide_info("WSI")
        return self.slide_info

    def get_info(self):
        if "WSI" in self.image_names:
            return self.get_slide_info()
        else:
            return slide_utils.get_error_response(status_code=500, detail="File does not contain WSI metadata")

    def get_region(
        self,
        level: int,
        start_x: int,
        start_y: int,
        size_x: int,
        size_y: int,
        image_format: str,
        image_quality: int,
        image_channels: List[int] = None,
        padding_color: tuple = None,
        z: int = 0,
    ):
        if image_format == "tiff":
            return (
                slide_utils.get_error_response(
                    status_code=400, detail="Output format 'tiff' is currently not supported for isyntax plugin"
                ),
                None,
            )

        data, region = self.__get_region(
            level=level,
            start_x=start_x,
            start_y=start_y,
            size_x=size_x,
            size_y=size_y,
            image_channels=image_channels,
            padding_color=padding_color,
            z=z,
        )

        if data["rep"] == "error":
            return data, region

        return slide_utils.get_success_response_with_payload(
            content={
                "media_type": f"image/{image_format}",
            },
            raw_payload=slide_utils.image_to_byte_array(region, image_format, image_quality),
        )

    def get_thumbnail(self, max_x: int, max_y: int, image_format: str, image_quality: int):
        if image_format == "tiff":
            return (
                slide_utils.get_error_response(
                    status_code=400, detail="Output format 'tiff' is currently not supported for isyntax plugin"
                ),
                None,
            )

        slide_info = self.get_slide_info()
        thumb_level = len(slide_info["content"]["levels"]) - 1
        for i, level in enumerate(slide_info["content"]["levels"]):
            if level["extent"]["x"] < max_x or level["extent"]["y"] < max_y:
                thumb_level = i
                break
        level_extent_x = int(slide_info["content"]["levels"][thumb_level]["extent"]["x"])
        level_extent_y = int(slide_info["content"]["levels"][thumb_level]["extent"]["y"])

        data, region = self.__get_region(
            level=thumb_level, start_x=0, start_y=0, size_x=level_extent_x, size_y=level_extent_y
        )

        if data["rep"] == "error":
            return data, region

        region.thumbnail((max_x, max_y))

        return slide_utils.get_success_response_with_payload(
            content={
                "media_type": f"image/{image_format}",
            },
            raw_payload=slide_utils.image_to_byte_array(region, image_format, image_quality),
        )

    def _get_associated_image(self, associated_image_name):
        if associated_image_name in self.image_names and self.pe_input[associated_image_name] is not None:
            pixel_data = self.pe_input[associated_image_name].image_data
            return (slide_utils.get_success_response(content={}), pixel_data)
        else:
            return (
                slide_utils.get_error_response(
                    status_code=500,
                    detail=f"Associated image {associated_image_name} does not exist.",
                ),
                None,
            )

    def get_label(self, max_x: int, max_y: int, image_format: str, image_quality: int):
        if image_format == "tiff":
            return (
                slide_utils.get_error_response(
                    status_code=400, detail="Output format 'tiff' is currently not supported for isyntax plugin"
                ),
                None,
            )

        data, raw_image_data = self._get_associated_image("LABELIMAGE")
        if data["rep"] == "error":
            return data, raw_image_data

        label_image_data = Image.open(BytesIO(raw_image_data))
        label_image_data.thumbnail((max_x, max_y))
        data["content"]["media_type"] = f"image/{image_format}"
        return data, slide_utils.image_to_byte_array(label_image_data, image_format, image_quality)

    def get_macro(self, max_x: int, max_y: int, image_format: str, image_quality: int):
        if image_format == "tiff":
            return (
                slide_utils.get_error_response(
                    status_code=400, detail="Output format 'tiff' is currently not supported for isyntax plugin"
                ),
                None,
            )

        data, raw_image_data = self._get_associated_image("MACROIMAGE")
        if data["rep"] == "error":
            return data, raw_image_data

        macro_image_data = Image.open(BytesIO(raw_image_data))
        macro_image_data.thumbnail((max_x, max_y))
        data["content"]["media_type"] = f"image/{image_format}"
        return data, slide_utils.image_to_byte_array(macro_image_data, image_format, image_quality)

    @cached(cache=LRUCache(maxsize=100))
    def get_tile(
        self,
        level: int,
        tile_x: int,
        tile_y: int,
        image_format: str,
        image_quality: int,
        image_channels: List[int] = None,
        padding_color: tuple = None,
        z: int = 0,
    ):
        if image_format == "tiff":
            return (
                slide_utils.get_error_response(
                    status_code=400, detail="Output format 'tiff' is currently not supported for isyntax plugin"
                ),
                None,
            )

        slide_info = self.get_slide_info()
        return self.get_region(
            level=level,
            start_x=tile_x * slide_info["content"]["tile_extent"]["x"],
            start_y=tile_y * slide_info["content"]["tile_extent"]["y"],
            size_x=slide_info["content"]["tile_extent"]["x"],
            size_y=slide_info["content"]["tile_extent"]["y"],
            image_format=image_format,
            image_quality=image_quality,
            image_channels=image_channels,
            padding_color=padding_color,
            z=z,
        )

    # private members

    def __get_region(
        self,
        level: int,
        start_x: int,
        start_y: int,
        size_x: int,
        size_y: int,
        image_channels: List[int] = None,
        padding_color: tuple = None,
        z: int = 0,
    ):
        if padding_color is None:
            padding_color = self.padding_color

        image = self.pe_input["WSI"]
        slide_info = self.get_slide_info()

        if slide_info["content"]["num_levels"] <= level:
            return (
                slide_utils.get_error_response(
                    status_code=422,
                    detail=f"""The requested pyramid level is not available.
                        The coarsest available level is {len(slide_info["content"]["levels"]) - 1}.""",
                ),
                None,
            )

        view_range_start_x = start_x
        view_range_start_y = start_y
        if start_x < 0 or start_y < 0:
            view_range_start_x = start_x if start_x >= 0 else 0
            view_range_start_y = start_y if start_y >= 0 else 0

        view_range = [
            view_range_start_x * (2**level),
            (view_range_start_x + size_x) * (2**level),
            view_range_start_y * (2**level),
            (view_range_start_y + size_y) * (2**level),
            level,
        ]

        try:
            # get data envelopes for requested levels
            data_envelopes = image.source_view.data_envelopes(level)
            _ = image.source_view.request_regions(
                [view_range], data_envelopes, False, [padding_color[0], padding_color[1], padding_color[2]]
            )
            # we only requested on region so we need to wait here until region is ready
            region = self.pixel_engine.wait_any()[0]
            pixel_buffer_size, patch_width, patch_height = self.__calculate_patch_size(image.source_view, region)

            raw_pixel_data = np.empty(int(pixel_buffer_size), dtype=np.uint8)
            region.get(raw_pixel_data)

            result_image = Image.frombuffer("RGB", (patch_width, patch_height), raw_pixel_data, "raw", "RGB", 0, 1)
            if start_x < 0 or start_y < 0:
                paste_coord_x = abs(start_x) if start_x < 0 else 0
                paste_coord_y = abs(start_y) if start_y < 0 else 0
                assembled_image = Image.new(mode="RGB", size=(size_x, size_y), color=padding_color)
                assembled_image.paste(result_image, (paste_coord_x, paste_coord_y))
                result_image = assembled_image

            if patch_width > size_x or patch_height > size_y:
                result_image = result_image.crop((0, 0, size_x, size_y))

            if image_channels:
                result_image = slide_utils.process_image_channels(result_image, image_channels)

            return slide_utils.get_success_response_with_payload(content={}, raw_payload=result_image)
        except RuntimeError as ex:
            return (
                slide_utils.get_error_response(status_code=500, detail=f"Philips SDK error [{ex}]"),
                None,
            )

    def __get_slide_levels(self, image):
        derived_levels = self.pe_input[image].source_view.num_derived_levels
        levels = []
        for resolution in range(derived_levels):
            dim = self.pe_input[image].source_view.dimension_ranges(resolution)
            # we need to calculate level dimensions for x and y manually
            dim_x = (dim[0][2] - dim[0][0]) / dim[0][1]
            dim_y = (dim[1][2] - dim[1][0]) / dim[1][1]
            levels.append(
                {
                    "extent": {"x": dim_x, "y": dim_y, "z": 1},
                    "downsample_factor": (2**resolution),
                }
            )

        return levels, derived_levels

    def __get_pixel_size(self, image):
        units = self.pe_input[image].source_view.dimension_units
        scale = self.pe_input[image].source_view.scale

        if units[0] == "MicroMeter":
            pixel_size_nm_x = scale[0] * 1000
            pixel_size_nm_y = scale[1] * 1000
        else:
            # other units supported?
            pixel_size_nm_x = scale[0]
            pixel_size_nm_y = scale[1]

        return {"x": pixel_size_nm_x, "y": pixel_size_nm_y}

    def __get_slide_info(self, image):
        levels, len_levels = self.__get_slide_levels(image)
        extent = self.pe_input[image].source_view.pixel_size

        block_size = self.pe_input[image].block_size(0)
        tile_extent = {"x": block_size[0], "y": block_size[1], "z": 1}
        if block_size[0] < 256:
            # If the size of the tile extent is smaller than 256 pixels, we increase
            # the width and length artificially to 256. This is especially useful for
            # viewer performance, as requesting many small tiles is way more
            # expensive than lesser large tiles.
            tile_extent = {"x": 256, "y": 256, "z": 1}

        try:
            slide_info = {
                "id": "slide_id",
                "channels": slide_utils.get_rgb_channel_dict(),
                "channel_depth": 8,
                "extent": {"x": extent[0], "y": extent[1], "z": 1},
                "pixel_size_nm": self.__get_pixel_size(image),
                "tile_extent": tile_extent,
                "num_levels": len_levels,
                "levels": levels,
                "format": "isyntax-isyntax",
            }
            return slide_utils.get_success_response(content=slide_info)
        except Exception as ex:
            return slide_utils.get_error_response(
                status_code=500, detail=f"Failed to gather slide info from file [{ex}]."
            )

    def __get_backends(self, back_end):
        for b_end in backends:
            if b_end.name == back_end:
                return b_end.backend(), b_end.context()
        return None

    def __calculate_patch_size(self, view, region):
        x_start, x_end, y_start, y_end, level = region.range
        dim_ranges = view.dimension_ranges(level)
        patch_width, patch_height = self.__calc_patch_width_height(x_start, x_end, y_start, y_end, dim_ranges)
        pixel_buffer_size = patch_width * patch_height * 3
        return pixel_buffer_size, patch_width, patch_height

    def __calc_patch_width_height(self, x_start, x_end, y_start, y_end, dim_ranges):
        patch_width = int(1 + (x_end - x_start) / dim_ranges[0][1])
        patch_height = int(1 + (y_end - y_start) / dim_ranges[1][1])
        return patch_width, patch_height


# rendering backends
class Backend:
    def __init__(self, name, context, backend):
        self.name = name
        self.context = context[0]
        self.backend = backend[0]
        self.contextclass = context[1]
        self.backendclass = backend[1]


backends = [
    Backend(
        "SOFTWARE",
        ["softwarerendercontext", "SoftwareRenderContext"],
        ["softwarerenderbackend", "SoftwareRenderBackend"],
    ),
    Backend(
        "GLES2",
        ["eglrendercontext", "EglRenderContext"],
        ["gles2renderbackend", "Gles2RenderBackend"],
    ),
    Backend(
        "GLES3",
        ["eglrendercontext", "EglRenderContext"],
        ["gles3renderbackend", "Gles3RenderBackend"],
    ),
]

# import backend libs if supported
valid_backends = []
for backend in backends:
    try:
        if backend.context not in sys.modules:
            contextlib = __import__(backend.context)
        if backend.backend not in sys.modules:
            backendlib = __import__(backend.backend)
    except RuntimeError:
        pass
    else:
        backend.context = getattr(contextlib, backend.contextclass)
        backend.backend = getattr(backendlib, backend.backendclass)
        valid_backends.append(backend)
backends = valid_backends
