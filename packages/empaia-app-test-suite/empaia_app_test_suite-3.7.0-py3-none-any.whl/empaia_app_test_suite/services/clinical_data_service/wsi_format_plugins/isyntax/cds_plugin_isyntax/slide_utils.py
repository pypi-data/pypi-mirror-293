import io
from typing import List

from PIL import Image


def get_rgb_channel_dict():
    channels = [
        {"id": 0, "name": "Red", "color": {"r": 255, "g": 0, "b": 0, "a": 0}},
        {"id": 1, "name": "Green", "color": {"r": 0, "g": 255, "b": 0, "a": 0}},
        {"id": 2, "name": "Blue", "color": {"r": 0, "g": 0, "b": 255, "a": 0}},
    ]
    return channels


def image_to_byte_array(image: Image, image_format: str, image_quality: int) -> bytes:
    # TODO: for now we don't support tiff files for isyntax
    # if image_format == "tiff":
    #    narray = np.asarray(image)
    #    narray = np.ascontiguousarray(narray.transpose(2, 0, 1))
    #    image = Image.fromarray(narray)

    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format=image_format, quality=image_quality)
    return img_byte_array.getvalue()


def process_image_channels(image: Image, image_channels: List[int]) -> Image:
    r = 1 if 0 in image_channels else 0
    g = 1 if 1 in image_channels else 0
    b = 1 if 2 in image_channels else 0
    conv_matrix = (r, 0, 0, 0, 0, g, 0, 0, 0, 0, b, 0)
    converted_image = image.convert("RGB", conv_matrix)
    return converted_image


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
