import datetime
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import Field

from ..commons import RestrictedBaseModel


class FHIRResourceType(str, Enum):
    QUESTIONNAIRE = "Questionnaire"
    QUESTIONNAIRE_RESPONSE = "QuestionnaireResponse"


class FHIRQuestionnaireStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RETIRED = "retired"
    UNKNOWN = "unknown"


class FHIRQuestionnaireResponseStatus(str, Enum):
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    AMENDED = "amended"
    ENTERED_IN_ERROR = "entered-in-error"
    STOPPED = "stopped"


# Base


class FHIRBackboneBaseModel(RestrictedBaseModel):
    id: str = Field(default=None, examples=["sample-id"], alias="id", description="ID of the FHIR resource")
    extension: Optional[Any] = Field(
        default=None, examples=[None], alias="extension", description="Additional content defined by implementations"
    )
    modifier_extension: Optional[Any] = Field(
        default=None, examples=[None], alias="modifierExtension", description="Extensions that cannot be ignored"
    )


class FHIRDomainBaseModel(FHIRBackboneBaseModel):
    meta: Optional[Any] = Field(default=None, examples=[None], alias="meta", description="Metadata of the resource")
    language: Optional[str] = Field(default=None, alias="language", description="Language of the resource content")
    contained: Optional[Any] = Field(
        default=None, examples=[None], alias="contained", description="Contained, inline Resources"
    )
    text: Optional[Any] = Field(
        default=None,
        examples=[None],
        alias="text",
        description="Text summary of the resource, for human interpretation",
    )


# Common


class Period(RestrictedBaseModel):
    resource_type: Literal["Period"] = Field(None, alias="resourceType")
    start: datetime.date = Field(default=None, examples=["2024-07-17"], alias="start", description="Start time")
    end: datetime.date = Field(default=None, examples=["2024-07-17"], alias="end", description="End time")


class Identifier(RestrictedBaseModel):
    resource_type: Literal["Identifier"] = Field(None, alias="resourceType")
    assigner: Optional[str] = Field(
        default=None, examples=["Organization"], alias="assigner", description="Organization that issued id"
    )
    period: Optional[Period] = Field(
        default=None, alias="period", description="Time period when id is/was valid for use"
    )
    system: Optional[str] = Field(
        default=None,
        examples=["http://terminology.hl7.org/CodeSystem/v2-0203"],
        alias="system",
        description="Identity of the terminology system",
    )
    type: Optional[str] = Field(default=None, examples=["MR"], alias="type", description="Description of identifier")
    use: Optional[str] = Field(
        default=None,
        alias="use",
        description="The purpose of this identifier",
        json_schema_extra={"enum_values": ["usual", "official", "temp", "secondary", "old"]},
    )
    value: Optional[str] = Field(
        default=None, examples=["some value"], alias="value", description="The value that is unique"
    )


class Coding(RestrictedBaseModel):
    resource_type: Literal["Coding"] = Field(None, alias="resourceType")
    code: Optional[str] = Field(
        default=None, examples=["example-code"], alias="code", description="Symbol in syntax defined by the system"
    )
    display: Optional[str] = Field(
        default=None,
        examples=["Example Display Text"],
        alias="display",
        description="Representation defined by the system",
    )
    system: Optional[str] = Field(
        default=None,
        examples=["http://example.com/system"],
        alias="system",
        description="Identity of the terminology system",
    )
    user_selected: Optional[bool] = Field(
        default=None,
        examples=[True],
        alias="userSelected",
        description="If this coding was chosen directly by the user",
    )
    version: Optional[str] = Field(
        default=None, examples=["v1"], alias="version", description="Version of the system - if relevant"
    )


class Reference(RestrictedBaseModel):
    reference: Optional[str] = Field(
        default=None,
        examples=["Patient/example"],
        alias="reference",
        description="Literal reference, relative, internal or absolute URL",
    )
    type: Optional[str] = Field(
        default=None, examples=["Patient"], alias="type", description="Type the reference refers to"
    )
    identifier: Optional[Identifier] = Field(
        default=None, alias="identifier", description="Logical reference, when literal reference is not known"
    )
    display: Optional[str] = Field(
        default=None, examples=["Example Display"], alias="display", description="Text alternative for the resource"
    )
