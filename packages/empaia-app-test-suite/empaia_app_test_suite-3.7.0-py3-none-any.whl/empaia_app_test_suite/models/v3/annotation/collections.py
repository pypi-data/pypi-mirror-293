from __future__ import annotations

from enum import Enum
from typing import Annotated, List, Literal, Optional, Union

from pydantic import UUID4, Field, ValidationError, field_validator, model_validator

from ..commons import (
    DataCreatorType,
    Description,
    Id,
    IdObject,
    ItemCount,
    Message,
    Name,
    PostIdObjects,
    RestrictedBaseModel,
    Viewport,
    validate_reference,
)
from .annotations import (
    AnnotationListResponse,
    ArrowAnnotation,
    CircleAnnotation,
    LineAnnotation,
    NppViewing,
    PointAnnotation,
    PolygonAnnotation,
    PostArrowAnnotation,
    PostCircleAnnotation,
    PostLineAnnotation,
    PostPointAnnotation,
    PostPolygonAnnotation,
    PostRectangleAnnotation,
    RectangleAnnotation,
)
from .classes import Class, ClassListResponse, PostClass
from .commons import PostValidationBase
from .pixelmaps import (
    ContinuousPixelmap,
    DiscretePixelmap,
    NominalPixelmap,
    PixelmapList,
    PostContinuousPixelmap,
    PostDiscretePixelmap,
    PostNominalPixelmap,
)
from .primitives import (
    BoolPrimitive,
    FloatPrimitive,
    IntegerPrimitive,
    PostBoolPrimitive,
    PostFloatPrimitive,
    PostIntegerPrimitive,
    PostStringPrimitive,
    PrimitiveList,
    StringPrimitive,
)


class CollectionItemType(str, Enum):
    WSI = "wsi"
    INTEGER = "integer"
    FLOAT = "float"
    BOOL = "bool"
    STRING = "string"
    POINT = "point"
    LINE = "line"
    ARROW = "arrow"
    CIRCLE = "circle"
    RECTANGLE = "rectangle"
    POLYGON = "polygon"
    CLASS = "class"
    CONTINUOUS = "continuous_pixelmap"
    DISCRETE = "discrete_pixelmap"
    NOMINAL = "nominal_pixelmap"
    COLLECTION = "collection"


class CollectionReferenceType(str, Enum):
    ANNOTATION = "annotation"
    WSI = "wsi"


# Item type models


class SlideItem(RestrictedBaseModel):
    id: Id = Field(examples=["4967bf63-a2a1-421c-8789-bf616953537c"], description="WSI ID")
    type: Literal["wsi"] = Field(examples=["wsi"], description="WSI type")


TYPE_MAPPING = {
    "point": PostPointAnnotation,
    "line": PostLineAnnotation,
    "arrow": PostArrowAnnotation,
    "circle": PostCircleAnnotation,
    "rectangle": PostRectangleAnnotation,
    "polygon": PostPolygonAnnotation,
    "class": PostClass,
    "integer": PostIntegerPrimitive,
    "float": PostFloatPrimitive,
    "bool": PostBoolPrimitive,
    "string": PostStringPrimitive,
    "wsi": SlideItem,
    "continuous_pixelmap": PostContinuousPixelmap,
    "discrete_pixelmap": PostDiscretePixelmap,
    "nominal_pixelmap": PostNominalPixelmap,
}


def check_items(items, type_name):
    if items and len(items) > 0:
        if not TYPE_MAPPING[type_name].model_validate(items[0]):
            raise ValidationError()
    return items


class PostPointAnnotationItems(PostValidationBase):
    items: Optional[List[PostPointAnnotation]] = Field(default=None, description="List of point annotations")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "point")


class PostLineAnnotationsItems(PostValidationBase):
    items: Optional[List[PostLineAnnotation]] = Field(default=None, description="List of line annotations")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "line")


class PostArrowAnnotationsItems(PostValidationBase):
    items: Optional[List[PostArrowAnnotation]] = Field(default=None, description="List of arrow annotations")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "arrow")


class PostCircleAnnotationsItems(PostValidationBase):
    items: Optional[List[PostCircleAnnotation]] = Field(default=None, description="List of circle annotations")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "circle")


class PostRectangleAnnotationsItems(PostValidationBase):
    items: Optional[List[PostRectangleAnnotation]] = Field(default=None, description="List of rectangle annotations")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "rectangle")


class PostPolygonAnnotationsItems(PostValidationBase):
    items: Optional[List[PostPolygonAnnotation]] = Field(default=None, description="List of polygon annotations")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "polygon")


class PostClassesItems(PostValidationBase):
    items: Optional[List[PostClass]] = Field(default=None, description="List of classes")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "class")


class PostIntegerPrimitivesItems(PostValidationBase):
    items: Optional[List[PostIntegerPrimitive]] = Field(default=None, description="List of integer primitives")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "integer")


class PostFloatPrimitivesItems(PostValidationBase):
    items: Optional[List[PostFloatPrimitive]] = Field(default=None, description="List of float primitives")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "float")


class PostBoolPrimitivesItems(PostValidationBase):
    items: Optional[List[PostBoolPrimitive]] = Field(default=None, description="List of bool primitives")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "bool")


class PostStringPrimitivesItems(PostValidationBase):
    items: Optional[List[PostStringPrimitive]] = Field(default=None, description="List of string primitives")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "string")


class PostContinuousPixelmapsItems(PostValidationBase):
    items: Optional[List[PostContinuousPixelmap]] = Field(default=None, description="List of continuous pixelmaps")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "continuous_pixelmap")


class PostDiscretePixelmapsItems(PostValidationBase):
    items: Optional[List[PostDiscretePixelmap]] = Field(default=None, description="List of discrete pixelmaps")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "discrete_pixelmap")


class PostNominalPixelmapsItems(PostValidationBase):
    items: Optional[List[PostNominalPixelmap]] = Field(default=None, description="List of nominal pixelmaps")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "nominal_pixelmap")


class PostSlideItems(PostValidationBase):
    items: Optional[List[SlideItem]] = Field(default=None, description="List of items")

    @field_validator("items", mode="before")
    @classmethod
    def pre_check_item_list(cls, v):
        return check_items(v, "wsi")


class SlideItemList(PostSlideItems):
    item_count: ItemCount = Field(examples=[12345], description="Count of all items")
    items: List[SlideItem] = Field(description="List of items")


# Post models


class PostCollectionBase(PostValidationBase):
    id: Optional[UUID4] = Field(
        default=None,
        examples=["4967bf63-a2a1-421c-8789-bf616953537c"],
        description="ID of type UUID4 (only needed in post if external Ids enabled)",
    )
    type: Literal["collection"] = Field(examples=["collection"], description="Collection type")
    name: Optional[Name] = Field(default=None, examples=["Collection Name"], description="Collection name")
    description: Optional[Description] = Field(
        default=None, examples=["Collection Description"], description="Collection description"
    )
    creator_id: Id = Field(
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="Creator Id",
    )
    creator_type: DataCreatorType = Field(examples=[DataCreatorType.JOB], description="Creator type")
    reference_id: Optional[Id] = Field(
        default=None,
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="Id of the object referenced by this collection",
    )
    reference_type: Optional[CollectionReferenceType] = Field(
        default=None, examples=[CollectionReferenceType.WSI], description="Refrence type"
    )

    # validator for reference
    @model_validator(mode="before")
    def check_reference(cls, data):
        reference_type = "reference_type" in data
        reference_id = "reference_id" in data
        validate_reference(reference_id=reference_id, reference_type=reference_type)
        return data


class PostPointCollection(PostCollectionBase, PostPointAnnotationItems):
    item_type: Literal["point"] = Field(examples=["point"], description="Item type of collection")


class PostLineCollection(PostCollectionBase, PostLineAnnotationsItems):
    item_type: Literal["line"] = Field(examples=["line"], description="Item type of collection")


class PostArrowCollection(PostCollectionBase, PostArrowAnnotationsItems):
    item_type: Literal["arrow"] = Field(examples=["arrow"], description="Item type of collection")


class PostCirceCollection(PostCollectionBase, PostCircleAnnotationsItems):
    item_type: Literal["circle"] = Field(examples=["circle"], description="Item type of collection")


class PostRectangleCollection(PostCollectionBase, PostRectangleAnnotationsItems):
    item_type: Literal["rectangle"] = Field(examples=["rectangle"], description="Item type of collection")


class PostPolygonCollection(PostCollectionBase, PostPolygonAnnotationsItems):
    item_type: Literal["polygon"] = Field(examples=["polygon"], description="Item type of collection")


class PostClassCollection(PostCollectionBase, PostClassesItems):
    item_type: Literal["class"] = Field(examples=["class"], description="Item type of collection")


class PostIntegerCollection(PostCollectionBase, PostIntegerPrimitivesItems):
    item_type: Literal["integer"] = Field(examples=["integer"], description="Item type of collection")


class PostFloatCollection(PostCollectionBase, PostFloatPrimitivesItems):
    item_type: Literal["float"] = Field(examples=["float"], description="Item type of collection")


class PostBoolCollection(PostCollectionBase, PostBoolPrimitivesItems):
    item_type: Literal["bool"] = Field(examples=["bool"], description="Item type of collection")


class PostStringCollection(PostCollectionBase, PostStringPrimitivesItems):
    item_type: Literal["string"] = Field(examples=["string"], description="Item type of collection")


class PostContinuousPixelmapCollection(PostCollectionBase, PostContinuousPixelmapsItems):
    item_type: Literal["continuous_pixelmap"] = Field(
        examples=["continuous_pixelmap"], description="Item type of collection"
    )


class PostDiscretePixelmapCollection(PostCollectionBase, PostDiscretePixelmapsItems):
    item_type: Literal["discrete_pixelmap"] = Field(
        examples=["discrete_pixelmap"], description="Item type of collection"
    )


class PostNominalPixelmapCollection(PostCollectionBase, PostNominalPixelmapsItems):
    item_type: Literal["nominal_pixelmap"] = Field(examples=["nominal_pixelmap"], description="Item type of collection")


class PostSlideCollection(PostCollectionBase, PostSlideItems):
    item_type: Literal["wsi"] = Field(examples=["wsi"], description="Item type of collection")


class PostIdCollection(PostCollectionBase, PostIdObjects):
    item_type: CollectionItemType = Field(examples=[CollectionItemType.POINT], description="Item type of collection")


class PostNestedCollectionBase(PostCollectionBase):
    item_type: Literal["collection"] = Field(examples=["collection"], description="Item type of collection")


class PostNestedItems(PostValidationBase):
    items: Optional[
        List[
            Union[
                PostPointCollection,
                PostLineCollection,
                PostArrowCollection,
                PostCirceCollection,
                PostRectangleCollection,
                PostPolygonCollection,
                PostClassCollection,
                PostIntegerCollection,
                PostFloatCollection,
                PostBoolCollection,
                PostStringCollection,
                PostContinuousPixelmapCollection,
                PostDiscretePixelmapCollection,
                PostNominalPixelmapCollection,
                PostSlideCollection,
                PostIdCollection,
                PostNestedCollection,
            ]
        ]
    ] = Field(default=None, description="List of items")


class PostNestedItemsApps(PostValidationBase):
    items: Optional[
        List[
            Union[
                PostPointCollection,
                PostLineCollection,
                PostArrowCollection,
                PostCirceCollection,
                PostRectangleCollection,
                PostPolygonCollection,
                PostClassCollection,
                PostIntegerCollection,
                PostFloatCollection,
                PostBoolCollection,
                PostStringCollection,
                PostContinuousPixelmapCollection,
                PostDiscretePixelmapCollection,
                PostNominalPixelmapCollection,
                PostNestedCollection,
            ]
        ]
    ] = Field(default=None, description="List of items")


class PostNestedCollection(PostNestedCollectionBase, PostNestedItems):
    pass


PostNestedCollection.model_rebuild()


class PostNestedCollectionApps(PostNestedCollectionBase, PostNestedItemsApps):
    pass


PostNestedCollectionApps.model_rebuild()


PostCollection = Union[
    PostPointCollection,
    PostLineCollection,
    PostArrowCollection,
    PostCirceCollection,
    PostRectangleCollection,
    PostPolygonCollection,
    PostClassCollection,
    PostIntegerCollection,
    PostFloatCollection,
    PostBoolCollection,
    PostStringCollection,
    PostContinuousPixelmapCollection,
    PostDiscretePixelmapCollection,
    PostNominalPixelmapCollection,
    PostSlideCollection,
    PostIdCollection,
    PostNestedCollection,
]


PostCollectionApps = Union[
    PostPointCollection,
    PostLineCollection,
    PostArrowCollection,
    PostCirceCollection,
    PostRectangleCollection,
    PostPolygonCollection,
    PostClassCollection,
    PostIntegerCollection,
    PostFloatCollection,
    PostBoolCollection,
    PostStringCollection,
    PostContinuousPixelmapCollection,
    PostDiscretePixelmapCollection,
    PostNominalPixelmapCollection,
    PostNestedCollectionApps,
]


class PostCollections(PostNestedItems):
    pass


class PostCollectionsApps(PostNestedItemsApps):
    pass


# Full model


class Collection(PostCollectionBase):
    item_type: CollectionItemType = Field(examples=[CollectionItemType.POINT], description="Item type of collection")
    is_locked: Optional[bool] = Field(
        default=None,
        examples=["false"],
        description="Flag to mark a collection as immutable",
    )
    item_count: Optional[ItemCount] = Field(
        default=None, examples=[42], description="The number of items in the collection"
    )
    items: Optional[
        Union[
            List[PointAnnotation],
            List[LineAnnotation],
            List[ArrowAnnotation],
            List[CircleAnnotation],
            List[RectangleAnnotation],
            List[PolygonAnnotation],
            List[Class],
            List[IntegerPrimitive],
            List[FloatPrimitive],
            List[BoolPrimitive],
            List[StringPrimitive],
            List[ContinuousPixelmap],
            List[DiscretePixelmap],
            List[NominalPixelmap],
            List[SlideItem],
            List[IdObject],
            List[Collection],
        ]
    ] = Field(default=None, description="Items of the collection")
    item_ids: Optional[List[UUID4]] = Field(
        default=None,
        description="Ids of items in collection",
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
    )


Collection.model_rebuild()


class CollectionList(RestrictedBaseModel):
    item_count: ItemCount = Field(examples=[12345], description="Count of items.")
    items: List[Collection] = Field(description="List of items.")


# Query model


class CollectionQuery(RestrictedBaseModel):
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
        description="List of reference Ids",
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
    item_types: Optional[Annotated[List[CollectionItemType], Field(min_length=1)]] = Field(
        default=None,
        examples=[[CollectionItemType.INTEGER, CollectionItemType.FLOAT]],
        description="List of item types",
    )


# Item models


PostItem = Union[
    PostPointAnnotation,
    PostLineAnnotation,
    PostArrowAnnotation,
    PostCircleAnnotation,
    PostRectangleAnnotation,
    PostPolygonAnnotation,
    PostClass,
    PostIntegerPrimitive,
    PostFloatPrimitive,
    PostBoolPrimitive,
    PostStringPrimitive,
    PostContinuousPixelmap,
    PostDiscretePixelmap,
    PostNominalPixelmap,
    SlideItem,
    IdObject,
    PostCollection,
]


PostItemList = Union[
    PostPointAnnotationItems,
    PostLineAnnotationsItems,
    PostArrowAnnotationsItems,
    PostCircleAnnotationsItems,
    PostRectangleAnnotationsItems,
    PostPolygonAnnotationsItems,
    PostClassesItems,
    PostIntegerPrimitivesItems,
    PostFloatPrimitivesItems,
    PostBoolPrimitivesItems,
    PostStringPrimitivesItems,
    PostContinuousPixelmapsItems,
    PostDiscretePixelmapsItems,
    PostNominalPixelmapsItems,
    PostSlideItems,
    PostIdObjects,
    PostCollections,
]

PostItemListApps = Union[
    PostPointAnnotationItems,
    PostLineAnnotationsItems,
    PostArrowAnnotationsItems,
    PostCircleAnnotationsItems,
    PostRectangleAnnotationsItems,
    PostPolygonAnnotationsItems,
    PostClassesItems,
    PostIntegerPrimitivesItems,
    PostFloatPrimitivesItems,
    PostBoolPrimitivesItems,
    PostStringPrimitivesItems,
    PostContinuousPixelmapsItems,
    PostDiscretePixelmapsItems,
    PostNominalPixelmapsItems,
    PostCollections,
]


PostItems = Union[PostItemList, PostItem]


class ItemQueryList(RestrictedBaseModel):
    item_count: ItemCount = Field(examples=[12345], description="Count of all items")
    items: Union[
        List[IntegerPrimitive],
        List[FloatPrimitive],
        List[BoolPrimitive],
        List[StringPrimitive],
        List[PointAnnotation],
        List[LineAnnotation],
        List[ArrowAnnotation],
        List[CircleAnnotation],
        List[RectangleAnnotation],
        List[PolygonAnnotation],
        List[Class],
        List[ContinuousPixelmap],
        List[DiscretePixelmap],
        List[NominalPixelmap],
        List[Collection],
    ] = Field(description="Items returned by item query")


ItemPostResponse = Union[
    Message,
    PointAnnotation,
    LineAnnotation,
    ArrowAnnotation,
    CircleAnnotation,
    RectangleAnnotation,
    PolygonAnnotation,
    AnnotationListResponse,
    IntegerPrimitive,
    FloatPrimitive,
    BoolPrimitive,
    StringPrimitive,
    PrimitiveList,
    Class,
    ClassListResponse,
    ContinuousPixelmap,
    DiscretePixelmap,
    NominalPixelmap,
    PixelmapList,
    SlideItem,
    SlideItemList,
    Collection,
    CollectionList,
]


# Item query model


class ItemQuery(RestrictedBaseModel):
    references: Optional[Annotated[List[Id], Field(min_length=1)]] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of reference Ids",
    )
    viewport: Optional[Viewport] = Field(
        default=None,
        examples=[{"x": 180, "y": 240, "width": 1280, "height": 1024}],
        description="The viewport (only used for annotations: only annotations within are returned)",
    )
    npp_viewing: Optional[NppViewing] = Field(
        default=None,
        examples=[[499.0, 7984.0]],
        description="Resolution range in npp (nanometer per pixel) to filter annotations (only used for annotations)",
    )
