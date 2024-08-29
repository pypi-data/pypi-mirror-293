import datetime
from typing import Any, List, Literal, Optional, Union

from pydantic import Field

from ..commons import RestrictedBaseModel
from ..fhir.commons import (
    Coding,
    FHIRBackboneBaseModel,
    FHIRDomainBaseModel,
    FHIRQuestionnaireStatus,
    Identifier,
    Period,
    Reference,
)


class QuestionnaireItemAnswerOption(RestrictedBaseModel):
    resource_type: Literal["QuestionnaireItemAnswerOption"] = Field(None, alias="resourceType")
    initial_selected: Optional[bool] = Field(
        default=None, alias="initialSelected", description="Whether option is selected by default"
    )
    value_coding: Optional[Coding] = Field(
        default=None,
        alias="valueCoding",
        description="Answer value coding",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    value_date: Optional[datetime.date] = Field(
        default=None,
        examples=["2024-07-17"],
        alias="valueDate",
        description="Answer value date",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    value_integer: Optional[int] = Field(
        default=None,
        examples=[42],
        alias="valueInteger",
        description="Answer value integer",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    value_reference: Optional[Reference] = Field(
        default=None,
        alias="valueReference",
        description="Answer value reference",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    value_string: Optional[str] = Field(
        default=None,
        examples=["example string"],
        alias="valueString",
        description="Answer value string",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    value_time: Optional[datetime.time] = Field(
        default=None,
        examples=["12:34:56"],
        alias="valueTime",
        description="Answer value time",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )


class QuestionnaireItemEnableWhen(RestrictedBaseModel):
    resource_type: Literal["QuestionnaireItemEnableWhen"] = Field(None, alias="resourceType")
    answer_boolean: Optional[bool] = Field(
        default=None,
        examples=[True],
        alias="answerBoolean",
        description="Value for question comparison based on operator",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    answer_coding: Optional[Coding] = Field(
        default=None,
        alias="answerCoding",
        description="Value for question comparison based on operator",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    answer_date: Optional[datetime.date] = Field(
        default=None,
        examples=["2024-07-17"],
        alias="answerDate",
        description="Value for question comparison based on operator",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    answer_date_time: Optional[datetime.datetime] = Field(
        default=None,
        examples=["2024-07-17T12:34:56"],
        alias="answerDateTime",
        description="Value for question comparison based on operator",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    answer_decimal: Optional[float] = Field(
        default=None,
        examples=[3.14],
        alias="answerDecimal",
        description="Value for question comparison based on operator",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    answer_integer: Optional[int] = Field(
        default=None,
        examples=[42],
        alias="answerInteger",
        description="Value for question comparison based on operator",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    answer_quantity: Optional[int] = Field(
        default=None,
        examples=[10],
        alias="answerQuantity",
        description="Value for question comparison based on operator",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    answer_reference: Optional[Reference] = Field(
        default=None,
        alias="answerReference",
        description="Value for question comparison based on operator",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    answer_string: Optional[str] = Field(
        default=None,
        examples=["example string"],
        alias="answerString",
        description="Value for question comparison based on operator",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    answer_time: Optional[datetime.time] = Field(
        default=None,
        examples=["12:34:56"],
        alias="answerTime",
        description="Value for question comparison based on operator",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    operator: Any = Field(
        default=None,
        examples=["="],
        alias="operator",
        description="Specifies the criteria by which the question is enabled",
        json_schema_extra={"enum_values": ["exists", "=", "!=", "\u003e", "\u003c", "\u003e=", "\u003c="]},
    )
    question: str = Field(
        default=None,
        examples=["link1"],
        alias="question",
        description="The linkId of question that determines whether item is " "enabled/disabled",
    )


class QuestionnaireItemInitial(RestrictedBaseModel):
    resource_type: Literal["QuestionnaireItemInitial"] = Field(None, alias="resourceType")
    value_attachment: Optional[Any] = Field(
        default=None,
        examples=[{"contentType": "application/pdf", "data": "SGVsbG8gV29ybGQ="}],
        alias="valueAttachment",
        description="Actual value for initializing the question",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    value_boolean: Optional[bool] = Field(
        default=None,
        examples=[True],
        alias="valueBoolean",
        description="Actual value for initializing the question",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    value_coding: Optional[Coding] = Field(
        default=None,
        alias="valueCoding",
        description="Actual value for initializing the question",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    value_date: Optional[datetime.date] = Field(
        default=None,
        examples=["2024-07-17"],
        alias="valueDate",
        description="Actual value for initializing the question",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    value_date_time: Optional[datetime.datetime] = Field(
        default=None,
        examples=["2024-07-17T12:34:56"],
        alias="valueDateTime",
        description="Actual value for initializing the question",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    value_decimal: Optional[float] = Field(
        default=None,
        examples=[3.14],
        alias="valueDecimal",
        description="Actual value for initializing the question",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    value_integer: Optional[int] = Field(
        default=None,
        examples=[42],
        alias="valueInteger",
        description="Actual value for initializing the question",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    value_quantity: Optional[float] = Field(
        default=None,
        examples=[5.0],
        alias="valueQuantity",
        description="Actual value for initializing the question",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    value_reference: Optional[Reference] = Field(
        default=None,
        alias="valueReference",
        description="Actual value for initializing the question",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    value_string: Optional[str] = Field(
        default=None,
        examples=["example string"],
        alias="valueString",
        description="Actual value for initializing the question",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    value_time: Optional[datetime.time] = Field(
        default=None,
        examples=["12:34:56"],
        alias="valueTime",
        description="Actual value for initializing the question",
        json_schema_extra={"one_of_many": "value", "one_of_many_required": True},
    )
    value_uri: Optional[Any] = Field(
        default=None,
        examples=["http://example.com"],
        alias="valueUri",
        description="Actual value for initializing the question",
    )


class PostQuestionnaireItem(RestrictedBaseModel):
    resource_type: Literal["QuestionnaireItem"] = Field(None, alias="resourceType")
    answer_constraint: Optional[Coding] = Field(default=None, alias="answerConstraint", description="Answer constraint")
    answer_option: Optional[List[QuestionnaireItemAnswerOption]] = Field(
        default=None,
        examples=[[{"valueString": "sample answer option"}]],
        alias="answerOption",
        description="Permitted answer",
    )
    answer_value_set: Optional[Union[Any, List[Any]]] = Field(
        default=None,
        examples=[None],
        alias="answerValueSet",
        description="Valueset containing permitted answers",
    )
    definition: Optional[Any] = Field(
        default=None,
        examples=[None],
        alias="definition",
        description="ElementDefinition - details for the item",
    )
    enable_behavior: Optional[str] = Field(
        default=None,
        examples=["all"],
        alias="enableBehavior",
        description="Controls how multiple enableWhen values are interpreted",
        json_schema_extra={"enum_values": ["all", "any"]},
    )
    enable_when: Optional[List[QuestionnaireItemEnableWhen]] = Field(
        default=[],
        examples=[[{"answerBoolean": True, "operator": "exists", "question": "link1"}]],
        alias="enableWhen",
        description="Only allow data when",
    )
    initial: Optional[List[QuestionnaireItemInitial]] = Field(
        default=[],
        examples=[[{"valueString": "sample initial answer"}]],
        alias="initial",
        description="Initial value(s) when item is first rendered",
    )
    # item type has to be of type `Any` to prevent circular referencing
    item: Optional[List[Any]] = Field(
        default=[], alias="item", description="QuestionnaireItem within the Questionnaire"
    )
    link_id: Optional[str] = Field(
        default=None, examples=["link1"], alias="linkId", description="Unique id for item in questionnaire"
    )
    repeats: Optional[bool] = Field(
        default=None, examples=["true"], alias="repeats", description="Whether the item may repeat"
    )
    required: Optional[bool] = Field(
        default=None,
        examples=["true"],
        alias="required",
        description="Whether the item must be included in data results",
    )
    text: Optional[str] = Field(None, alias="text", description="Primary text for the item")
    type: str = Field(
        default="group",
        examples=["display"],
        alias="type",
        description="The type of questionnaire item",
        json_schema_extra={
            "enum_values": ["group", "display", "boolean", "decimal", "integer", "date", "dateTime", "choice"]
        },
    )


class QuestionnaireItem(FHIRBackboneBaseModel, PostQuestionnaireItem):
    code: Optional[List[Coding]] = Field(
        default=None, alias="code", description="Corresponding concept for this item in a terminology"
    )
    max_length: Optional[int] = Field(
        None, examples=[256], alias="maxLength", description="No more than this many characters"
    )
    prefix: Optional[str] = Field(
        None,
        alias="prefix",
        description="A short label for a particular group, question or set of display text within the questionnaire",
    )
    read_only: Optional[bool] = Field(
        default=None, examples=["true"], alias="readOnly", description="Don't allow human editing"
    )


class BaseQuestionnaire(RestrictedBaseModel):
    resource_type: Literal["Questionnaire"] = Field(None, alias="resourceType")
    approval_date: Optional[Union[datetime.date, int]] = Field(
        default=None,
        examples=["2024-07-17", 1720784354],
        alias="approvalDate",
        description="When the questionnaire was approved by publisher",
    )
    description: Optional[str] = Field(
        default=None,
        examples={"example string"},
        alias="description",
        description="Natural language description of the questionnaire",
    )
    identifier: Optional[List[Identifier]] = Field(
        default=None,
        examples=[[{"value": "dummy-identifier"}]],
        alias="identifier",
        description="Additional identifier for the questionnaire",
    )
    name: Optional[str] = Field(
        default=None, examples=["Name"], alias="name", description="Name for this questionnaire (computer friendly)"
    )
    publisher: Optional[str] = Field(
        default=None,
        examples=["Publisher name"],
        alias="publisher",
        description="Name of the publisher (organization or individual)",
    )
    status: FHIRQuestionnaireStatus = Field(
        default=FHIRQuestionnaireStatus.DRAFT,
        examples=[FHIRQuestionnaireStatus.DRAFT],
        alias="status",
        description="The current status of the questionnaire",
        # json_schema_extra={"enum_values": ["draft", "active", "retired", "unknown"]},
    )
    title: Optional[str] = Field(
        default=None, examples=["Example Questionnaire"], alias="title", description="Label for this questionnaire"
    )
    use_context: Optional[List[Any]] = Field(
        default=None,
        examples=[None],
        alias="useContext",
        description="The context that the content is intended to support",
    )


class PostQuestionnaire(BaseQuestionnaire):
    item: Optional[List[PostQuestionnaireItem]] = Field(
        default=None, alias="item", description="Questions and sections within the Questionnaire"
    )


class Questionnaire(FHIRDomainBaseModel, BaseQuestionnaire):
    code: Optional[List[Coding]] = Field(
        default=None, alias="code", description="Concept that represents the overall questionnaire"
    )
    contact: Optional[List[Any]] = Field(
        default=None, examples=[None], alias="contact", description="Contact details for the publisher"
    )
    copyright: Optional[Any] = Field(
        default=None, examples=[None], alias="copyright", description="Use and/or publishing restrictions"
    )
    date: Optional[datetime.date] = Field(
        default=None, examples=["2024-07-17"], alias="date", description="Date last changed"
    )
    derived_from: Optional[List[Any]] = Field(
        default=None, examples=[None], alias="derivedFrom", description="Instantiates protocol or definition"
    )
    effective_period: Optional[Period] = Field(
        default=None, alias="effectivePeriod", description="When the questionnaire is expected to be used"
    )
    experimental: Optional[bool] = Field(
        default=None, examples=[False], alias="experimental", description="For testing purposes, not real usage"
    )
    item: Optional[List[QuestionnaireItem]] = Field(
        default=None, alias="item", description="Questions and sections within the Questionnaire"
    )
    jurisdiction: Optional[List[Coding]] = Field(
        default=None,
        examples=[None],
        alias="jurisdiction",
        description="Intended jurisdiction for questionnaire (if applicable)",
    )
    last_review_date: Optional[datetime.date] = Field(
        default=None,
        examples=["2024-07-17"],
        alias="lastReviewDate",
        description="When the questionnaire was last reviewed",
    )
    name: Optional[str] = Field(
        default=None, examples=["Name"], alias="name", description="Name for this questionnaire (computer friendly)"
    )
    publisher: Optional[str] = Field(
        default=None,
        examples=["Publisher name"],
        alias="publisher",
        description="Name of the publisher (organization or individual)",
    )
    purpose: Optional[str] = Field(
        default=None, examples=["Some purpose"], alias="purpose", description="Why this questionnaire is needed"
    )
    subject_type: Optional[List[Any]] = Field(
        default=None,
        examples=[None],
        alias="subjectType",
        description="Resource that can be subject of QuestionnaireResponse",
    )
    title: Optional[str] = Field(
        default=None, examples=["Example Questionnaire"], alias="title", description="Label for this questionnaire"
    )
    url: Optional[str] = Field(
        default=None,
        examples=["http://example.com/questionnaire"],
        alias="url",
        description="Canonical URL for this questionnaire",
    )
    use_context: Optional[List[Any]] = Field(
        default=None,
        examples=[None],
        alias="useContext",
        description="The context that the content is intended to support",
    )
    version: Optional[str] = Field(
        default=None, examples=["1.0"], alias="version", description="The version of the questionnaire"
    )


class QuestionnaireList(RestrictedBaseModel):
    item_count: int = Field(description="Count of items")
    items: List[Questionnaire] = Field(default=None, description="List of questionnaires")


class QuestionnaireQuery(RestrictedBaseModel):
    questionnaires: Optional[List[str]] = Field(
        default=None, examples=[["1", "5", "24"]], alias="questionnaires", description="Filter by questionnaire IDs"
    )
    identifiers: Optional[List[str]] = Field(
        default=None,
        examples=[["ident1", "indent2"]],
        alias="identifiers",
        description="Filter by questionnaire identifiers",
    )
    statuses: Optional[List[FHIRQuestionnaireStatus]] = Field(
        default=None,
        examples=[[FHIRQuestionnaireStatus.DRAFT, FHIRQuestionnaireStatus.ACTIVE]],
        alias="statuses",
        description="Filter by questionnaire status",
    )
