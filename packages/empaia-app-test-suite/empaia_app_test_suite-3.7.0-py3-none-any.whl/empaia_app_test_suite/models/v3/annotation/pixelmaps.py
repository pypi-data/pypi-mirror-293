from enum import Enum
from typing import Annotated, Any, List, Literal, Optional, Union

from pydantic import UUID4, Field, ValidationError, field_validator, model_validator

from ...singletons import model_settings
from ..commons import ClassValue, DataCreatorType, Description, Id, ItemCount, Name, RestrictedBaseModel, Timestamp
from ..slide import SlideExtent, SlideLevel, SlidePixelSizeNm
from .commons import PostValidationBase

Tilesize = Annotated[int, Field(ge=256, le=2048, strict=True)]


def validate_values(min_value, max_value, neutral_value=None):
    if not (min_value < max_value):
        raise ValueError("Value contraint not met: min_value < max_value")
    if neutral_value:
        if not (min_value <= neutral_value <= max_value):
            raise ValueError("Value contraints not met: min_value <= neutral_value <= max_value")


class PixelmapReferenceType(str, Enum):
    WSI = "wsi"


class PixelmapType(str, Enum):
    CONTINUOUS = "continuous_pixelmap"
    DISCRETE = "discrete_pixelmap"
    NOMINAL = "nominal_pixelmap"


class NumberClassMapping(RestrictedBaseModel):
    class_value: Annotated[
        ClassValue,
        Field(examples=["org.empaia.my_vendor.my_app.v3.0.classes.non_tumor"], description="A valid class value."),
    ]
    number_value: Annotated[
        int, Field(ge=0, strict=True, examples=[0], description="The numeric value the class is mapped to.")
    ]


class PixelmapLevel(RestrictedBaseModel):
    slide_level: Annotated[int, Field(ge=0, strict=True, examples=[0], description="refers to a WSI level")]
    position_min_x: Annotated[
        Optional[int],
        Field(
            default=None,
            ge=0,
            strict=True,
            examples=[10],
            description="""
            Smallest x index of all tiles in the PixelmapLevel. Tiles to the left side of the index cannot be created. \
            Is used by viewers to avoid unnecessary requests for sparse data.
            """,
        ),
    ]
    position_min_y: Annotated[
        Optional[int],
        Field(
            default=None,
            ge=0,
            strict=True,
            examples=[5],
            description="""
            Smallest y index of all tiles in the PixelmapLevel. Tiles above the index cannot be created. Is used by \
            viewers to avoid unnecessary requests for sparse data.
            """,
        ),
    ]
    position_max_x: Annotated[
        Optional[int],
        Field(
            default=None,
            ge=0,
            strict=True,
            examples=[20],
            description="""
            Largest x index of all tiles in the PixelmapLevel. Tiles to the right side of the index cannot be created. \
            Is used by viewers to avoid unnecessary requests for sparse data.
            """,
        ),
    ]
    position_max_y: Annotated[
        Optional[int],
        Field(
            default=None,
            ge=0,
            strict=True,
            examples=[30],
            description="""
            Largest y index of all tiles in the PixelmapLevel. Tiles below the index cannot be created. Is used by \
            viewers to avoid unnecessary requests for sparse data.
            """,
        ),
    ]


# Validator to ensure slide_level values are only used once
def validate_levels(levels: List[PixelmapLevel]):
    level_values = []
    for level in levels:
        level_values.append(level.slide_level)
    if len(level_values) != len(set(level_values)):
        raise ValueError("Pixelmap level defined twice. Values for 'slide_level' must be unique!")


class PixelmapCore(RestrictedBaseModel):
    name: Name = Field(examples=["Pixelmap Name"], description="Pixelmap name")
    description: Optional[Description] = Field(
        default=None, examples=["Pixelmap Description"], description="Pixelmap description"
    )
    reference_id: Id = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="ID of referenced Slide")
    reference_type: PixelmapReferenceType = Field(
        examples=[PixelmapReferenceType.WSI], description='Reference type (must be "wsi")'
    )
    levels: Annotated[List[PixelmapLevel], Field(min_length=1)] = Field(
        description="""
        Meta data describing which WSI levels will receive Pixelmap tiles and in which region (position_min_x, \
        position_min_y, position_max_x, position_max_y) of the given level the Pixelmap tiles will be written. \
        This meta data serves as a hint for viewers to not request non-existing tiles outside these regions. \
        If a certain level will not receive Pixelmap data, it should not be added to the list.
        """,
    )
    channel_count: Annotated[
        int,
        Field(
            ge=0,
            strict=True,
            examples=[1],
            description="number of channels the Pixelmap contains (must be > 0)",
        ),
    ]
    tilesize: Tilesize = Field(
        examples=[512],
        description="The width and height of each tile (only squares allowed, 256 <= tilesize <= 2048).",
    )
    channel_class_mapping: Optional[List[NumberClassMapping]] = Field(
        default=None,
        description="""
        A dict that maps the index values of the channels to fully qualified class names to express the semantic \
        meaning of that channel.
        """,
    )

    # validator for levels
    @model_validator(mode="after")
    def check_levels(cls, data):
        is_post = str(cls).split(".")[-1].lower().startswith("post")
        if is_post and model_settings.disable_post_validation:
            return data
        validate_levels(data.levels)
        return data

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            value_list = []
            if isinstance(value, List):
                for v in value:
                    if isinstance(v, PixelmapLevel):
                        value_list.append(v.__dict__)
                result[key] = value_list
            else:
                result = self._to_dict_part(value, key, result)
        return result

    def _to_dict_part(self, value, key, result):
        if isinstance(value, Enum):
            result[key] = value.value
        elif hasattr(value, "to_dict"):
            result[key] = value.to_dict()
        else:
            result[key] = value
        return result


min_value_int = Annotated[
    int,
    Field(
        strict=True,
        examples=[-10],
        description="The minimum value of the Pixelmap pixel element data",
    ),
]

neutral_value_int = Annotated[
    int,
    Field(
        strict=True,
        examples=[0],
        description="The neutral value of the Pixelmap pixel element data",
    ),
]

max_value_int = Annotated[
    int,
    Field(
        strict=True,
        examples=[42],
        description="The maximum value of the Pixelmap pixel element data",
    ),
]

min_value_float = Annotated[
    float,
    Field(
        strict=True,
        examples=[-10.7],
        description="The minimum value of the Pixelmap pixel element data",
    ),
]

neutral_value_float = Annotated[
    float,
    Field(
        strict=True,
        examples=[0.0],
        description="The neutral value of the Pixelmap pixel element data",
    ),
]

max_value_float = Annotated[
    float,
    Field(
        strict=True,
        examples=[42.43],
        description="The maximum value of the Pixelmap pixel element data",
    ),
]


class ContinuousPixelmapElementType(str, Enum):
    _float32 = "float32"
    _float64 = "float64"


class ContinuousPixelmapCore(PixelmapCore):
    type: Literal["continuous_pixelmap"] = Field(
        examples=["continuous_pixelmap"], description="Continuous Pixelmap type"
    )
    element_type: ContinuousPixelmapElementType = Field(
        examples=["float32"],
        description="""
            The type of the scalar elements in the Pixelmap. All channels of a Pixelmap have the same element type.
            """,
    )
    min_value: min_value_float
    neutral_value: Optional[neutral_value_float] = Field(default=None)
    max_value: max_value_float

    # validator for min, max and neutral values
    @model_validator(mode="after")
    def check_values(cls, data):
        is_post = str(cls).split(".")[-1].lower().startswith("post")
        if is_post and model_settings.disable_post_validation:
            return data
        min_value = data.min_value
        max_value = data.max_value
        neutral_value = data.neutral_value
        validate_values(min_value=min_value, max_value=max_value, neutral_value=neutral_value)
        return data


class DiscretePixelmapElementType(str, Enum):
    _uint8 = "uint8"
    _uint16 = "uint16"
    _uint32 = "uint32"
    _uint64 = "uint64"
    _int8 = "int8"
    _int16 = "int16"
    _int32 = "int32"
    _int64 = "int64"


class DiscretePixelmapCore(PixelmapCore):
    type: Literal["discrete_pixelmap"] = Field(examples=["discrete_pixelmap"], description="Discrete Pixelmap type")
    element_type: DiscretePixelmapElementType = Field(
        examples=["int8"],
        description="""
        the type of the scalar elements in the Pixelmap. If the Pixelmap has multiple channels (a depth>1), they all \
        have the same element type.
        """,
    )
    min_value: min_value_int
    neutral_value: Optional[neutral_value_int] = Field(default=None)
    max_value: max_value_int
    element_class_mapping: Optional[List[NumberClassMapping]] = Field(
        default=None,
        description="""
        A dict that maps numeric values to fully qualified class names to express the semantic meaning of the values \
        in all channels. Note: only one mapping for all channels, make sure that the encoding does not overlap.
        """,
    )

    # validator for min, max and neutral values
    @model_validator(mode="after")
    def check_values(cls, data):
        is_post = str(cls).split(".")[-1].lower().startswith("post")
        if is_post and model_settings.disable_post_validation:
            return data
        min_value = data.min_value
        max_value = data.max_value
        neutral_value = data.neutral_value
        validate_values(min_value=min_value, max_value=max_value, neutral_value=neutral_value)
        return data


class NominalPixelmapElementType(str, Enum):
    _uint8 = "uint8"
    _uint16 = "uint16"
    _uint32 = "uint32"
    _uint64 = "uint64"
    _int8 = "int8"
    _int16 = "int16"
    _int32 = "int32"
    _int64 = "int64"


class NominalPixelmapCore(PixelmapCore):
    type: Literal["nominal_pixelmap"] = Field(examples=["nominal_pixelmap"], description="Nominal Pixelmap type")
    element_type: NominalPixelmapElementType = Field(
        examples=["uint8"],
        description="""
        The type of the scalar elements in the Pixelmap. All channels of a Pixelmap have the same element type.
        """,
    )
    neutral_value: Optional[neutral_value_int] = Field(default=None)
    element_class_mapping: List[NumberClassMapping] = Field(
        examples=[
            (
                "[{'number_value': 0, 'class_value': 'org.empaia.my_vendor.my_app.v3.0.classes.non_tumor'}, \\"
                "{'number_value': 1, 'class_value': 'org.empaia.my_vendor.my_app.v3.0.classes.tumor'}]"
            )
        ],
        description="""
        A dict that maps numeric values to fully qualified class names to express the semantic meaning of the values \
        in all channels. Note: only one mapping for all channels, make sure that the encoding does not overlap.
        """,
    )


# Post Models
class PostPixelmapBase(PostValidationBase):
    id: Optional[UUID4] = Field(
        default=None,
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="ID of type UUID4 (only needed in post if external Ids enabled)",
    )
    creator_id: Id = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="Creator ID")
    creator_type: DataCreatorType = Field(examples=[DataCreatorType.JOB], description="Creator type")


class PostContinuousPixelmap(PostPixelmapBase, ContinuousPixelmapCore):
    pass


class PostDiscretePixelmap(PostPixelmapBase, DiscretePixelmapCore):
    pass


class PostNominalPixelmap(PostPixelmapBase, NominalPixelmapCore):
    pass


PostPixelmap = Union[PostContinuousPixelmap, PostDiscretePixelmap, PostNominalPixelmap]


TYPE_MAPPING = {
    "continuous_pixelmap": PostContinuousPixelmap,
    "discrete_pixelmap": PostDiscretePixelmap,
    "nominal_pixelmap": PostNominalPixelmap,
}


def check_items(items, type_name):
    if len(items) > 0:
        if not TYPE_MAPPING[type_name].model_validate(items[0]):
            raise ValidationError()
    return items


class PostContinuousPixelmaps(RestrictedBaseModel):
    items: List[PostContinuousPixelmap] = Field(description="List of continous pixelmaps")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "continuous_pixelmap")


class PostDiscretePixelmaps(RestrictedBaseModel):
    items: List[PostDiscretePixelmap] = Field(description="List of discrete pixelmaps")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "discrete_pixelmap")


class PostNominalPixelmaps(RestrictedBaseModel):
    items: List[PostNominalPixelmap] = Field(description="List of nominal pixelmaps")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "nominal_pixelmap")


PostPixelmapList = Union[PostContinuousPixelmaps, PostDiscretePixelmaps, PostNominalPixelmaps]


PostPixelmaps = Union[PostPixelmapList, PostPixelmap]

# Full models:


class PixelmapBase(PostPixelmapBase):
    created_at: Timestamp = Field(examples=[1598611645], description="UNIX timestamp in seconds - set by server")
    updated_at: Timestamp = Field(examples=[1598611645], description="UNIX timestamp in seconds - set by server")


class ContinuousPixelmap(PixelmapBase, ContinuousPixelmapCore):
    pass


class DiscretePixelmap(PixelmapBase, DiscretePixelmapCore):
    pass


class NominalPixelmap(PixelmapBase, NominalPixelmapCore):
    pass


Pixelmap = Union[ContinuousPixelmap, DiscretePixelmap, NominalPixelmap]


class PixelmapList(RestrictedBaseModel):
    item_count: ItemCount = Field(examples=[12345], description="Count of all items")
    items: List[Pixelmap] = Field(description="List of items")


Pixelmaps = Union[Pixelmap, PixelmapList]


# Query models:


class PixelmapQuery(RestrictedBaseModel):
    creators: Optional[Annotated[List[Id], Field(min_length=1)]] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of creator Ids",
    )
    references: Optional[Annotated[List[Id], Field(min_length=1)]] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description=("List of reference Ids."),
    )
    jobs: Optional[Annotated[List[Id], Field(min_length=1)]] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of job Ids",
    )
    types: Optional[Annotated[List[PixelmapType], Field(min_length=1)]] = Field(
        default=None,
        examples=[[PixelmapType.CONTINUOUS, PixelmapType.DISCRETE]],
        description="List of pixelmap types",
    )
    pixelmaps: Optional[Annotated[List[Any], Field(min_length=1)]] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of Pixelmap Ids (must be of type UUID4)",
    )


# Update models:


class UpdatePixelmapCore(RestrictedBaseModel):
    name: Name = Field(examples=["Pixelmap Name"], description="Pixelmap name")
    description: Optional[Description] = Field(
        default=None, examples=["Pixelmap Description"], description="Pixelmap description"
    )
    channel_class_mapping: Optional[List[NumberClassMapping]] = Field(
        default=None,
        description="""
        A dict that maps the index values of the channels to fully qualified class names to express the semantic \
        meaning of that channel.
        """,
    )


class UpdateContinuousPixelmap(UpdatePixelmapCore):
    min_value: min_value_float
    neutral_value: Optional[neutral_value_float] = Field(default=None)
    max_value: max_value_float

    # validator for min, max and neutral values
    @model_validator(mode="after")
    def check_values(cls, data):
        min_value = data.min_value
        max_value = data.max_value
        neutral_value = data.neutral_value
        validate_values(min_value=min_value, max_value=max_value, neutral_value=neutral_value)
        return data


class UpdateDiscretePixelmap(UpdatePixelmapCore):
    min_value: min_value_int
    neutral_value: Optional[neutral_value_int] = Field(default=None)
    max_value: max_value_int
    element_class_mapping: Optional[List[NumberClassMapping]] = Field(
        default=None,
        description="""
        A dict that maps numeric values to fully qualified class names to express the semantic meaning of the values \
        in all channels. Note: only one mapping for all channels, make sure that the encoding does not overlap.
        """,
    )

    # validator for min, max and neutral values
    @model_validator(mode="after")
    def check_values(cls, data):
        min_value = data.min_value
        max_value = data.max_value
        neutral_value = data.neutral_value
        validate_values(min_value=min_value, max_value=max_value, neutral_value=neutral_value)
        return data


class UpdateNominalPixelmap(UpdatePixelmapCore):
    neutral_value: Optional[neutral_value_int] = Field(default=None)
    element_class_mapping: List[NumberClassMapping] = Field(
        description="""
        A dict that maps numeric values to fully qualified class names to express the semantic meaning of the values \
        in all channels. Note: only one mapping for all channels, make sure that the encoding does not overlap.
        """,
    )


UpdatePixelmap = Union[UpdateContinuousPixelmap, UpdateDiscretePixelmap, UpdateNominalPixelmap]


class PixelmapSlideInfo(RestrictedBaseModel):
    extent: SlideExtent = Field(..., description="Image extent (finest level, level=0)")
    num_levels: int = Field(..., description="Number of levels in image pyramid")
    pixel_size_nm: SlidePixelSizeNm = Field(..., description="Pixel size in nm  (finest level, level=0)")
    levels: List[SlideLevel]
