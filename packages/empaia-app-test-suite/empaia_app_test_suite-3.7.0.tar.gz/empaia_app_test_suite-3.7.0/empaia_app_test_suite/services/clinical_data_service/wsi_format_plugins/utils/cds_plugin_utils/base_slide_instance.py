# TODO: documentation
from typing import List


class BaseSlideInstance:
    def __init__(self, filepath: str, padding_color: tuple):
        pass

    def close(self):
        pass

    def get_info(self):
        pass

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
        pass

    def get_thumbnail(self, max_x: int, max_y: int, image_format: str, image_quality: int):
        pass

    def get_label(self, max_x: int, max_y: int, image_format: str, image_quality: int):
        pass

    def get_macro(self, max_x: int, max_y: int, image_format: str, image_quality: int):
        pass

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
        pass
