"""
Module defining the different models used in the Clinical Data Service.
At the moment, the model is simplified to just Cases and Slides, but it may get extended
to also include separate classes for Specimen, Blocks, Sections, and Stains. The model
is used both for the Data Base and for the JSON requests and responses of the REST API.
"""

from enum import Enum
from typing import Annotated, List, Optional

from pydantic import UUID4, Field

from .commons import Description, Id, ItemCount, RestrictedBaseModel, Timestamp


class CaseCreatorType(str, Enum):
    """Type of Case Creator"""

    USER = "USER"
    # AUTOMATIC = "AUTOMATIC"
    # SOLUTION = "SOLUTION"  # post-MVP


class PutClinicalSlide(RestrictedBaseModel):
    """Information for updating an existing Slide"""

    tissue: Optional[str] = Field(
        default=None,
        examples=["SKIN"],
        description="The type of tissue that can be seen in this Slide",
    )

    stain: Optional[str] = Field(
        default=None,
        examples=["HER2"],
        description="The stain that has been applied to the section",
    )

    block: Optional[str] = Field(
        default=None,
        examples=["some block"],
        description="The block this slide belongs to",
    )

    deleted: Optional[bool] = Field(
        default=None,
        examples=[False],
        description="Flag indicating whether the underlying slide files and mappings have been deleted",
    )

    __hash__ = object.__hash__


class PostClinicalSlideCore(PutClinicalSlide):
    """Information needed for creating a new Slide, excluding derived DB attributes"""

    id: Optional[UUID4] = Field(
        default=None,
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="Unique ID of the slide",
    )

    case_id: UUID4 = Field(
        ...,
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="The ID of the case this slide belongs to",
    )


class PostClinicalSlide(PostClinicalSlideCore):
    main_path: Optional[str] = Field(
        default=None,
        examples=["path/to/file_or_directory"],
        description="Main path to WSI that can be accessed by the Clinical Data Service",
    )


class ClinicalSlide(PostClinicalSlideCore):
    """Class representing an individual Slide. A Slide belongs to a specific Case, identified
    by its ID, and shows a specimen of a certain Tissue with some Stain applied to it.
    In this first version, all this information is contained directly within the Slide class,
    but might also be separated into individual Stain, Block, Specimen etc. classes later on.
    """

    created_at: Timestamp = Field(
        examples=[1623349180],
        description="Timestamp when the slide was created",
    )

    updated_at: Timestamp = Field(
        examples=[1623349180],
        description="Timestamp when the slide was last updated",
    )


class PutCase(RestrictedBaseModel):
    """Information for updating an existing Case"""

    description: Optional[Description] = Field(
        default=None,
        examples=["A very interesting example case"],
        description="Optional free-form textual description of the case",
    )

    deleted: Optional[bool] = Field(
        default=None,
        examples=[False],
        description="Flag indicating whether the underlying slide files and mappings have been deleted",
    )

    __hash__ = object.__hash__


class PostCase(PutCase):
    """Information needed for creating a new Case, excluding derived DB attributes"""

    id: Optional[UUID4] = Field(
        default=None,
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="Unique IDs of the Case",
    )

    creator_id: Id = Field(
        ...,
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="ID referring to the pathologist / EMPAIA user who created or 'owns' the case",
    )

    creator_type: CaseCreatorType = Field(
        ...,
        examples=[CaseCreatorType.USER],
        description="The type of creator, i.e. a user or an automatic process",
    )


class Case(PostCase):
    """Class representing a case. Not sure if we still need all those attributes that were previously
    defined for the first version for the MVP. I'll leave them in for now, but we can also remove them
    or set them to Optional.
    """

    created_at: Timestamp = Field(
        examples=[1623349180],
        description="Timestamp when the case was created",
    )

    updated_at: Timestamp = Field(
        examples=[1623349180],
        description="Timestamp when the case was last updated",
    )

    slides: Optional[List[ClinicalSlide]] = Field(
        default=None,
        description="The actual slides of the case",
    )


class CaseList(RestrictedBaseModel):
    """Wrapper for a collections of Cases, possibly filtered, including total count before paging"""

    item_count: ItemCount = Field(
        examples=[1],
        description="Total number of cases matching the query",
    )

    items: List[Case] = Field(
        examples=[
            [
                Case(
                    id="b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                    creator_id="b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                    creator_type=CaseCreatorType.USER,
                    created_at=1623349180,
                    updated_at=1623349180,
                )
            ]
        ],
        description="The actual cases",
    )


class ClinicalSlideList(RestrictedBaseModel):
    """Wrapper for a collections of Slides, possibly filtered, including total count before paging"""

    item_count: ItemCount = Field(
        examples=[1],
        description="Total number of slides matching the query",
    )

    items: List[ClinicalSlide] = Field(
        examples=[
            [
                ClinicalSlide(
                    id="b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                    case_id="b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                    tissue="SKIN",
                    stain="HER2",
                    block="some block",
                    deleted=False,
                    created_at=1623349180,
                    updated_at=1623349180,
                )
            ]
        ],
        description="The actual Slides",
    )


class ClinicalSlideQuery(RestrictedBaseModel):
    """Query for one or more slides by Case Id; more attributes might be added later, e.g. time ranges."""

    cases: Optional[Annotated[List[UUID4], Field(min_length=1)]] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of case Ids",
    )
