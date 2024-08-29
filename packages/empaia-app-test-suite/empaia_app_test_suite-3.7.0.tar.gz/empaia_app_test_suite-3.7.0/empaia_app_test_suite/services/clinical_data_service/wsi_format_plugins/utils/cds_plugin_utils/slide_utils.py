import io
from typing import List

import numpy as np
import tifffile
from PIL import Image


class UnsupportedOutputFormatError(Exception):
    pass


class UnsupportedArrayConversionError(Exception):
    pass


class TifffileWriteError(Exception):
    pass


def process_region_binary(
    narray: np.ndarray | np.generic, image_format: str, image_quality: int, image_channels: List[int]
):
    if image_format in ["jpeg", "png", "bmp", "gif"]:
        return process_image_pil(
            narray=narray, image_format=image_format, image_quality=image_quality, image_channels=image_channels
        )
    if image_format == "tiff":
        if image_channels:
            narray = get_requested_channels_as_array(narray, image_channels)
        return narray_to_tiff_byte_array(narray=narray)

    raise UnsupportedOutputFormatError(f"Output format {image_format} not supported by plugin")


def process_image_pil(
    narray: np.ndarray | np.generic, image_format: str, image_quality: int, image_channels: List[int]
):
    rgb_array = get_requested_channels_as_rgb_array(narray=narray, image_channels=image_channels)
    if image_channels is None:
        pil_image = convert_narray_to_pil_image(narray=rgb_array)
    else:
        mode = "L" if len(image_channels) == 1 else "RGB"
        pil_image = convert_narray_to_pil_image(
            narray=rgb_array, lower=np.min(rgb_array), upper=np.max(rgb_array), mode=mode
        )
    return image_to_byte_array(pil_image, image_format=image_format, image_quality=image_quality)


def get_requested_channels_as_array(narray: np.ndarray | np.generic, image_channels: List[int]):
    if narray.shape[0] == len(image_channels):
        return narray

    separate_channels = np.vsplit(narray, narray.shape[0])
    temp_array = [separate_channels[i] for i in image_channels]
    result = np.concatenate(temp_array, axis=0)
    return result


def convert_narray_to_pil_image(narray: np.ndarray | np.generic, lower=None, upper=None, mode="RGB"):
    if narray.dtype == np.uint8:
        narray_uint8 = narray
    elif narray.dtype == np.uint16:
        narray_uint8 = convert_narray_uintX_to_uint8(narray, 16, lower, upper)
    elif narray.dtype in [np.uint32, np.float32]:
        narray_uint8 = convert_narray_uintX_to_uint8(narray, 32, lower, upper)
    elif narray.dtype in [np.uint64, np.float64]:
        narray_uint8 = convert_narray_uintX_to_uint8(narray, 64, lower, upper)
    else:
        raise UnsupportedArrayConversionError(f"Array conversion for type {narray.dtype} not supported")

    try:
        if mode == "L":
            # convert to grayscale for single channel
            new_array = narray_uint8[0, :, :]
            pil_image = Image.fromarray(new_array, mode="L")
        else:
            # we need to transpose the array here to make it readable for pillow (width, height, channel)
            narray_uint8 = np.ascontiguousarray(narray_uint8.transpose(1, 2, 0))
            pil_image = Image.fromarray(narray_uint8, mode="RGB")
        return pil_image
    except ValueError as e:
        raise ValueError(f"Internal conversion to pillow image failed: {e}")


def convert_narray_uintX_to_uint8(narray: np.ndarray | np.generic, exp: int = 16, lower: int = None, upper: int = None):
    if exp not in [8, 16, 32, 64]:
        raise ValueError("Only exponent in range [8, 16, 32, 64] supported")
    if lower is not None and not (0 <= lower < 2**exp):
        raise ValueError(f"lower bound must be between 0 and 2**{exp}")
    if upper is not None and not (0 <= upper < 2**exp):
        raise ValueError(f"upper bound must be between 0 and 2**{exp}")
    if not lower and not upper and exp == 8:
        return narray
    if lower is None:
        lower = 0
    if upper is None:
        upper = (2**exp) - 1
        # default upper bound for bitness > 8 to enhance contrast/brightness
        if exp > 8:
            upper = (2**exp) / (exp / 4)

    temp_array = np.divide((narray - lower), (upper - lower))
    temp_array = np.clip(temp_array * 255, 0, 255)
    return temp_array.astype(np.uint8)


def get_requested_channels_as_rgb_array(narray: np.ndarray | np.generic, image_channels: List[int]):
    separate_channels = np.vsplit(narray, narray.shape[0])

    temp_array = []
    if image_channels is not None and len(image_channels) == 1:
        # edge case 1: single channel will be converted to a grayscale image
        return separate_channels[image_channels[0]]
    elif image_channels is not None and len(image_channels) == 2:
        # edge case 2: we cast two dedicated image to an rgb image if requested
        temp_array.append(separate_channels[image_channels[0]])
        temp_array.append(separate_channels[image_channels[1]])
        temp_array.append(np.zeros(separate_channels[image_channels[0]].shape))
    else:
        # three or more channels given
        # in this case we simply return the first 3 channels for now
        temp_array = get_multi_channel_as_rgb(separate_channels)

    result = np.concatenate(temp_array, axis=0)
    return result


def get_multi_channel_as_rgb(separate_channels):
    # right now only three channels are considered
    temp_array = []
    for channel in separate_channels:
        if len(temp_array) == 3:
            break
        temp_array.append(channel)
    return temp_array


def get_rgb_channel_dict():
    channels = [
        {"id": 0, "name": "Red", "color": {"r": 255, "g": 0, "b": 0, "a": 0}},
        {"id": 1, "name": "Green", "color": {"r": 0, "g": 255, "b": 0, "a": 0}},
        {"id": 2, "name": "Blue", "color": {"r": 0, "g": 0, "b": 255, "a": 0}},
    ]
    return channels


def get_tile_extent(tile_width, tile_height):
    tile_height = 256
    tile_width = 256

    # some tiles can have an unequal tile height and width that can cause problems in the slide viewer
    # since the tile route is soley used for viewing, we provide the default tile width and height
    if tile_width == tile_height:
        tile_width = tile_width
        tile_height = tile_height

    return {"x": tile_width, "y": tile_height, "z": 1}


def get_original_levels(level_count, level_dimensions, level_downsamples):
    levels = []
    for level in range(level_count):
        extent = {
            "x": level_dimensions[level][0],
            "y": level_dimensions[level][1],
            "z": 1,
        }
        levels.append({"extent": extent, "downsample_factor": level_downsamples[level]})
    return levels


def narray_to_tiff_byte_array(narray: np.ndarray | np.generic) -> bytes:
    mem = io.BytesIO()
    try:
        if narray.shape[0] == 1:
            tifffile.imwrite(mem, narray, photometric="minisblack", compression="DEFLATE")
        else:
            tifffile.imwrite(mem, narray, photometric="minisblack", planarconfig="separate", compression="DEFLATE")
    except Exception as ex:
        raise TifffileWriteError(status_code=400, detail=f"Error writing tiff file: {ex}")
    mem.seek(0)

    return mem.getvalue()


def image_to_byte_array(image: Image, image_format: str, image_quality: int) -> bytes:
    img_byte_array = io.BytesIO()
    if image_format.lower() == "tiff":
        img_array = np.asarray(image).transpose(2, 0, 1)
        planar_config = None if img_array.shape[0] == 1 else "separate"
        tifffile.imwrite(
            img_byte_array, img_array, photometric="minisblack", planarconfig=planar_config, compression="DEFLATE"
        )
        img_byte_array.seek(0)
    else:
        image.save(img_byte_array, format=image_format, quality=image_quality)
    return img_byte_array.getvalue()


def process_image_channels(image: Image, image_channels: List[int]) -> Image:
    r = 1 if 0 in image_channels else 0
    g = 1 if 1 in image_channels else 0
    b = 1 if 2 in image_channels else 0
    conv_matrix = (r, 0, 0, 0, 0, g, 0, 0, 0, 0, b, 0)
    converted_image = image.convert("RGB", conv_matrix)
    return converted_image


def rgba_to_rgb_with_background_color(image_rgba: Image, padding_color: tuple):
    if image_rgba.info.get("transparency", None) is not None or image_rgba.mode == "RGBA":
        image_rgb = Image.new("RGB", image_rgba.size, padding_color)
        image_rgb.paste(image_rgba, mask=image_rgba.split()[3])
    else:
        image_rgb = image_rgba.convert("RGB")
    return image_rgb


def check_region_overlaps_image(start_x, start_y, size_x, size_y, level_width, level_height):
    return start_x < 0 or start_y < 0 or (start_x + size_x) > level_width or (start_y + size_y) > level_height


def get_crop_region_coordinates(start_x, start_y, size_x, size_y, level_width, level_height):
    if start_x > level_width or start_y > level_height:
        return (0, 0, 0, 0)

    requested_region_start_x = start_x
    requested_region_start_y = start_y
    requested_region_size_x = size_x
    requested_region_size_y = size_y

    if start_x < 0:
        requested_region_start_x = 0
        requested_region_size_x -= abs(start_x)
    if start_y < 0:
        requested_region_start_y = 0
        requested_region_size_y -= abs(start_y)
    requested_region_size_x = min((requested_region_start_x + requested_region_size_x), level_width)
    requested_region_size_y = min((requested_region_start_y + requested_region_size_y), level_height)

    return (requested_region_start_x, requested_region_start_y, requested_region_size_x, requested_region_size_y)


def get_paste_region_coordinates(start_x, start_y, size_x, size_y):
    if (start_x + size_x) < 0 or (start_y + size_y) < 0:
        return (0, 0)

    paste_coord_x = 0
    paste_coord_y = 0

    if start_x < 0:
        paste_coord_x += abs(start_x)
    if start_y < 0:
        paste_coord_y += abs(start_y)

    return (paste_coord_x, paste_coord_y)


def calculate_thumbnail_size(original_width: int, original_height: int, max_width: int, max_height: int):
    aspect_ratio = original_width / original_height

    if original_width > max_width or original_height > max_height:
        if original_width / max_width > original_height / max_height:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
    else:
        new_width = original_width
        new_height = original_height

    return new_width, new_height


def get_error_response(status_code: int, detail: str):
    return {
        "rep": "error",
        "status_code": status_code,
        "detail": detail,
    }


def get_success_response(content: dict):
    return {
        "rep": "success",
        "status_code": 200,
        "content": content,
    }


def get_success_response_with_payload(content: dict, raw_payload=None):
    return (
        {
            "rep": "success",
            "status_code": 200,
            "content": content,
        },
        raw_payload,
    )
