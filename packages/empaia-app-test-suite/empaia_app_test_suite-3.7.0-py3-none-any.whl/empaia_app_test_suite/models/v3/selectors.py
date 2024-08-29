from sqlite3 import Timestamp
from typing import List, Literal, Optional

from pydantic import UUID4, Field

from ..commons import RestrictedBaseModel
from ..fhir.commons import FHIRResourceType


class PostSelector(RestrictedBaseModel):
    type: Literal[FHIRResourceType.QUESTIONNAIRE] = Field(
        description="Type of the respective FHIR resource (for now only type Questionnaire allowed)"
    )
    logical_id: str = Field(
        examples=["sample-resource-id"],
        description="Logical ID of the FHIR resource (must match a valid FHIR resource)",
    )
    selector_value: str = Field(
        examples=["org.vendor.app.iccr_breast"], description="Selector value choosen by EAD/user"
    )


class Selector(PostSelector):
    id: UUID4 = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="ID of the selector")
    created_at: Timestamp = Field(examples=[1598611645], description="UNIX timestamp in seconds - set by server")


class SelectorList(RestrictedBaseModel):
    item_count: int = Field(description="Count of items")
    items: List[Selector] = Field(default=None, description="List of selectors")


class PostSelectorTagging(RestrictedBaseModel):
    type: Literal[FHIRResourceType.QUESTIONNAIRE] = Field(
        description="Type of the respective FHIR resource (for now only type Questionnaire allowed)"
    )
    selector_value: str = Field(
        examples=["org.vendor.app.iccr_breast"], description="Selector value choosen by EAD/user"
    )
    indication: str = Field(examples=["ICCR_CARCINOMA_OF_BREAST"], description="Indication tag for a selector value")
    procedure: str = Field(examples=["MASTECTOMY"], description="Procedure tag for a selector value")


class SelectorTagging(PostSelectorTagging):
    id: UUID4 = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="ID of the selector")
    created_at: Timestamp = Field(examples=[1598611645], description="UNIX timestamp in seconds - set by server")


class SelectorTaggingList(RestrictedBaseModel):
    item_count: int = Field(description="Count of items")
    items: List[SelectorTagging] = Field(default=None, description="List of selector taggings")


class SelectorQuery(RestrictedBaseModel):
    types: Optional[List[FHIRResourceType]] = Field(
        default=None,
        examples=[[FHIRResourceType.QUESTIONNAIRE]],
        alias="types",
        description="Filter by FHIR resource types",
    )
    selectors: Optional[List[str]] = Field(
        default=None,
        examples=[["b10648a7-340d-43fc-a2d9-4d91cc86f33f"]],
        alias="selectors",
        description="Filter by selector IDs",
    )
    selector_values: Optional[List[str]] = Field(
        default=None,
        examples=[["org.vendor.app.iccr_breast"]],
        alias="selector_values",
        description="Filter by selector values",
    )
