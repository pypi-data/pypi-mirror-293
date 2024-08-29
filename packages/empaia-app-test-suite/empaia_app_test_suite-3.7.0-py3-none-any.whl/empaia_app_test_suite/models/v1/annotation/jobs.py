from enum import Enum
from typing import Annotated, List, Literal, Union

from pydantic import Field

from ..commons import Id, ItemCount, RestrictedBaseModel
from .collections import CollectionItems


class JobLock(RestrictedBaseModel):
    item_id: Id = Field(
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="ID of the locked element",
    )
    job_id: Id = Field(
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="ID of the job the element was locked for",
    )


class NodeType(str, Enum):
    ANNOTATION = "annotation"
    WSI = "wsi"


class ReferenceData(RestrictedBaseModel):
    item_count: ItemCount = Field(examples=[12345], description="Count of all items")
    items: CollectionItems = Field(description="List of items.")


class PrimitiveDetails(RestrictedBaseModel):
    reference_type: Union[Literal["collection"], None] = Field(
        examples=["collection"],
        description=(
            "Reference type of primitive (can only be collection or null). "
            "IMPORTANT NOTE: can be null, if specified primitive does not have a reference (reference_id is not set)!"
        ),
    )
    reference_data: Union[ReferenceData, None] = Field(
        description=(
            "If reference type is collection: the items of the referenced collection. "
            "IMPORTANT NOTE: can be null, if specified primitive does not have a reference (reference_id is not set)!"
        ),
    )


class TreeNodeItemDetails(RestrictedBaseModel):
    node_id: Id = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="The ID of the tree node")
    node_type: NodeType = Field(examples=[NodeType.WSI], description="The node type of the tree node")
    position: Annotated[int, Field(ge=0)] = Field(
        examples=[5], description="The position of the node in the item list of its parent"
    )


class TreeNodeSequence(RestrictedBaseModel):
    node_sequence: List[TreeNodeItemDetails] = Field(
        examples=[
            [
                {"node_id": "b10648a7-340d-43fc-a2d9-4d91cc86f33f", "node_type": "wsi", "position": 0},
                {"node_id": "b10648a7-340d-43fc-a2d9-4d91cc86f33f", "node_type": "annotation", "position": 2},
                {"node_id": "b10648a7-340d-43fc-a2d9-4d91cc86f33f", "node_type": "annotation", "position": 634},
            ]
        ],
        description="The tree node sequence",
    )
