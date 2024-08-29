import datetime
from typing import Any, List, Literal, Optional

from pydantic import Field

from ..commons import RestrictedBaseModel
from ..fhir.commons import (
    Coding,
    FHIRBackboneBaseModel,
    FHIRDomainBaseModel,
    FHIRQuestionnaireResponseStatus,
    Reference,
)


class QuestionnaireResponseItemAnswer(RestrictedBaseModel):
    resource_type: Literal["QuestionnaireResponseItemAnswer"] = Field(None, alias="resourceType")
    valueBoolean: Optional[bool] = Field(
        default=None, examples=[True], alias="valueBoolean", description="Single-valued answer to the question"
    )
    valueDecimal: Optional[float] = Field(
        default=None, examples=[3.14], alias="valueDecimal", description="Single-valued answer to the question"
    )
    valueInteger: Optional[int] = Field(
        default=None, examples=[42], alias="valueInteger", description="Single-valued answer to the question"
    )
    valueDate: Optional[datetime.date] = Field(
        default=None, examples=["2024-07-17"], alias="valueDate", description="Single-valued answer to the question"
    )
    valueDateTime: Optional[datetime.datetime] = Field(
        default=None,
        examples=["2024-07-17T12:34:56"],
        alias="valueDateTime",
        description="Single-valued answer to the question",
    )
    valueTime: Optional[datetime.time] = Field(
        default=None, examples=["12:34:56"], alias="valueTime", description="Single-valued answer to the question"
    )
    valueString: Optional[str] = Field(
        default=None,
        examples=["example string"],
        alias="valueString",
        description="Single-valued answer to the question",
    )
    valueUri: Optional[str] = Field(
        default=None,
        examples=["http://example.com"],
        alias="valueUri",
        description="Single-valued answer to the question",
    )
    valueAttachment: Optional[Any] = Field(
        default=None, alias="valueAttachment", description="Single-valued answer to the question"
    )
    valueCoding: Optional[Coding] = Field(
        default=None,
        examples=[{"code": "example-code", "display": "Example Display", "system": "http://example.com/system"}],
        alias="valueCoding",
        description="Single-valued answer to the question",
    )
    valueQuantity: Optional[Any] = Field(
        default=None, examples=[5.0], alias="valueQuantity", description="Single-valued answer to the question"
    )
    valueReference: Optional[Reference] = Field(
        default=None,
        examples=[{"reference": "Patient/example"}],
        alias="valueReference",
        description="Single-valued answer to the question",
    )


class BaseQuestionnaireResponseItem(RestrictedBaseModel):
    resource_type: Literal["QuestionnaireResponseItem"] = Field(None, alias="resourceType")
    answer: Optional[List[QuestionnaireResponseItemAnswer]] = Field(
        default=[],
        examples=[[{"valueString": "sample answer"}]],
        alias="answer",
        description="The response(s) to the question",
    )
    definition: Optional[Any] = Field(
        default=None,
        examples=[None],
        alias="definition",
        description="ElementDefinition - details for the item",
    )
    link_id: str = Field(
        default=None, examples=["link1"], alias="linkId", description="Unique id for item in questionnaire response"
    )
    text: Optional[str] = Field(
        default=None, examples=["This is a question"], alias="text", description="Name for this item"
    )


class PostQuestionnaireResponseItem(BaseQuestionnaireResponseItem):
    item: Optional[List["PostQuestionnaireResponseItem"]] = Field(
        default=[], alias="item", description="Questions or sub-groups nested beneath a question"
    )


class QuestionnaireResponseItem(FHIRBackboneBaseModel, BaseQuestionnaireResponseItem):
    item: Optional[List["QuestionnaireResponseItem"]] = Field(
        default=[], alias="item", description="Questions or sub-groups nested beneath a question"
    )


class BaseQuestionnaireResponse(RestrictedBaseModel):
    resource_type: Literal["QuestionnaireResponse"] = Field(None, alias="resourceType")
    questionnaire: Optional[str] = Field(
        default=None,
        examples=["Questionnaire/questionnaire-id"],
        alias="questionnaire",
        description="The Questionnaire that defines and organizes the questions",
    )
    status: FHIRQuestionnaireResponseStatus = Field(
        default=FHIRQuestionnaireResponseStatus.COMPLETED,
        examples=[FHIRQuestionnaireResponseStatus.COMPLETED],
        alias="status",
        description="The current state of the questionnaire response",
        # json_schema_extra={"enum_values": ["in-progress", "completed", "amended", "entered-in-error", "stopped"]},
    )
    authored: Optional[datetime.date] = Field(
        default=None,
        examples=["2024-07-17"],
        alias="authored",
        description="Date the answers were gathered",
    )
    # keep?
    author: Optional[Reference] = Field(
        default=None,
        examples=[{"reference": "Practitioner/example"}],
        alias="author",
        description="Person who received and recorded the answers",
    )


class PostQuestionnaireResponse(BaseQuestionnaireResponse):
    item: Optional[List[PostQuestionnaireResponseItem]] = Field(
        default=None,
        alias="item",
        description="Groups and questions",
    )


class QuestionnaireResponse(FHIRDomainBaseModel, BaseQuestionnaireResponse):
    based_on: Optional[List[Reference]] = Field(
        default=None,
        examples=[{"reference": "ServiceRequest/example"}],
        alias="basedOn",
        description="Request fulfilled by this QuestionnaireResponse",
    )
    part_of: Optional[List[Reference]] = Field(
        default=None, examples=[{"reference": "Observation/example"}], alias="partOf", description="Part of this action"
    )
    subject: Optional[Reference] = Field(
        default=None,
        examples=[{"reference": "Patient/example"}],
        alias="subject",
        description="The subject of the questionnaire response",
    )
    encounter: Optional[Reference] = Field(
        default=None,
        examples=[{"reference": "Encounter/example"}],
        alias="encounter",
        description="Encounter created as part of",
    )
    source: Optional[Reference] = Field(
        default=None,
        examples=[{"reference": "Patient/example"}],
        alias="source",
        description="The person who answered the questions",
    )
    item: Optional[List[QuestionnaireResponseItem]] = Field(
        default=None,
        alias="item",
        description="Groups and questions",
    )


class QuestionnaireResponseList(RestrictedBaseModel):
    item_count: int = Field(description="Count of items")
    items: List[QuestionnaireResponse] = Field(default=None, description="List of questionnaire responses")


class QuestionnaireResponseQuery(RestrictedBaseModel):
    questionnaire_responses: Optional[List[str]] = Field(
        default=None,
        examples=[["1", "5", "24"]],
        alias="questionnaireReponses",
        description="Filter by questionnaire response IDs",
    )
    # questionnaires: Optional[List[str]] = Field(
    #     default=None, examples=[["1", "5", "24"]], alias="questionnaires", description="Filter by questionnaire IDs"
    # )
    identifiers: Optional[List[str]] = Field(
        default=None,
        examples=[["ident1", "indent2"]],
        alias="identifiers",
        description="Filter by questionnaire response identifiers",
    )
    statuses: Optional[List[FHIRQuestionnaireResponseStatus]] = Field(
        default=None,
        examples=[[FHIRQuestionnaireResponseStatus.COMPLETED, FHIRQuestionnaireResponseStatus.IN_PROGRESS]],
        alias="statuses",
        description="Filter by questionnaire response status",
    )
