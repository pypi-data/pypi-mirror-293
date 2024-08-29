from enum import Enum
from typing import Annotated, List, Optional

from pydantic import UUID4, BaseModel, ConfigDict, Field

Id = Annotated[str, Field(min_length=1, max_length=50, json_schema_extra={"strip_whitespace": True})]
Name = Annotated[str, Field(min_length=1, max_length=200, json_schema_extra={"strip_whitespace": True})]
Description = Annotated[str, Field(min_length=1, max_length=1000, json_schema_extra={"strip_whitespace": True})]
ClassValue = Annotated[str, Field(min_length=1, max_length=100, json_schema_extra={"strip_whitespace": True})]
Timestamp = Annotated[int, Field(ge=0)]
ItemCount = Annotated[int, Field(ge=0)]


class DataCreatorType(str, Enum):
    JOB = "job"
    USER = "user"
    SCOPE = "scope"


class DataReferenceType(str, Enum):
    WSI = "wsi"
    ANNOTATION = "annotation"
    COLLECTION = "collection"
    NONE = None


class RestrictedBaseModel(BaseModel):
    """Abstract Super-class not allowing unknown fields in the **kwargs."""

    model_config = ConfigDict(extra="forbid")


class Message(RestrictedBaseModel):
    message: str = Field(description="Message used for untyped responses")


class Detail(RestrictedBaseModel):
    detail: str = Field(description="Message used for untyped responses")


class IdObject(RestrictedBaseModel):
    id: Id = Field(
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="ID (type string) of a single element",
    )


class Viewport(RestrictedBaseModel):
    x: Annotated[
        int,
        Field(
            ge=0,
            strict=True,
            examples=[180],
            description="X coordinate of upper left corner of viewport (must be >= 0)",
        ),
    ]
    y: Annotated[
        int,
        Field(
            ge=0,
            strict=True,
            examples=[240],
            description="Y coordinate of upper left corner of viewport (must be >= 0)",
        ),
    ]
    width: Annotated[int, Field(ge=0, strict=True, examples=[1280], description="Width of viewport (must be > 0)")]
    height: Annotated[int, Field(ge=0, strict=True, examples=[1024], description="Height of viewport (must be > 0)")]


class UniqueReferences(RestrictedBaseModel):
    annotation: Optional[List[UUID4]] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of unique referenced annotation IDs (type UUID4)",
    )
    collection: Optional[List[UUID4]] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of unique referenced collection IDs (type UUID4)",
    )
    wsi: Optional[List[Id]] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of unique referenced WSI IDs (type string)",
    )
    contains_items_without_reference: Optional[bool] = Field(
        default=None,
        examples=[True],
        description="If true: there are items matching the filter criteria without a reference",
    )


# Shared validator for reference of collection and primitive


def validate_reference(reference_id, reference_type):
    if (not reference_id and reference_type) or (reference_id and not reference_type):
        raise ValueError(
            "The fields reference_id and reference_type must either both be None or set with valid values!"
        )
