from enum import Enum
from typing import Annotated, Any, List, Literal, Optional, Union

from pydantic import UUID4, Field

from ..commons import (
    ClassValue,
    DataCreatorType,
    Description,
    Id,
    ItemCount,
    Name,
    RestrictedBaseModel,
    Timestamp,
    Viewport,
)
from .classes import Class

NppCreated = Annotated[float, Field(gt=0.0)]
NppViewing = Annotated[List[Annotated[float, Field(gt=0.0)]], Field(min_length=2, max_length=2)]
UniqueClassValue = Union[ClassValue, None]
Coordinate = Annotated[int, Field(ge=0, strict=True)]
Point = Annotated[List[Coordinate], Field(min_length=2, max_length=2)]
Line = Annotated[List[Point], Field(min_length=2, max_length=2)]
Polygon = Annotated[List[Point], Field(min_length=3)]


class AnnotationType(str, Enum):
    POINT = "point"
    LINE = "line"
    ARROW = "arrow"
    CIRCLE = "circle"
    RECTANGLE = "rectangle"
    POLYGON = "polygon"


class AnnotationReferenceType(str, Enum):
    WSI = "wsi"


# Core models - used by AppService


class AnnotationCore(RestrictedBaseModel):
    name: Name = Field(examples=["Annotation Name"], description="Annotation name")
    description: Optional[Description] = Field(
        default=None, examples=["Annotation Description"], description="Annotation description"
    )
    reference_id: Id = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="ID of referenced Slide")
    reference_type: AnnotationReferenceType = Field(
        examples=[AnnotationReferenceType.WSI], description='Reference type (must be "wsi")'
    )
    npp_created: NppCreated = Field(
        examples=[499.0],
        description="Resolution in npp (nanometer per pixel) used to indicate on which layer the annotation is created",
    )
    npp_viewing: Optional[NppViewing] = Field(
        default=None,
        examples=[[499.0, 7984.0]],
        description="Recommended viewing resolution range in npp (nanometer per pixel) - Can be set by app",
    )
    centroid: Optional[Point] = Field(
        default=None,
        examples=[[100, 100]],
        description="Centroid of the annotation",
    )


class PointAnnotationCore(AnnotationCore):
    type: Literal["point"] = Field(examples=["point"], description="Point annotation")
    coordinates: Point = Field(examples=[[100, 200]], description="Point coordinates (must be >= 0)")


class LineAnnotationCore(AnnotationCore):
    type: Literal["line"] = Field(examples=["line"], description="Line annotation")
    coordinates: Line = Field(examples=[[[0, 100], [100, 100]]], description="Line coordinates (must be >= 0)")


class ArrowAnnotationCore(AnnotationCore):
    type: Literal["arrow"] = Field(examples=["arrow"], description="Arrow annotation")
    head: Point = Field(examples=[[0, 100]], description="Point coordinates of arrow head (must be >= 0)")
    tail: Point = Field(examples=[[100, 150]], description="Point coordinates of arrow tail (must be >= 0)")


class CircleAnnotationCore(AnnotationCore):
    type: Literal["circle"] = Field(examples=["circle"], description="Circle annotation")
    center: Point = Field(examples=[[0, 100]], description="Point coordinates of center (must be >= 0)")
    radius: Annotated[int, Field(gt=0, strict=True)] = Field(examples=[100], description="Radius (must be > 0)")


class RectangleAnnotationCore(AnnotationCore):
    type: Literal["rectangle"] = Field(examples=["rectangle"], description="Rectangle annotation")
    upper_left: Point = Field(
        examples=[[0, 100]],
        description="Point coordinates of upper left corner of the rectangle (must be >= 0)",
    )
    width: Annotated[int, Field(gt=0, strict=True)] = Field(examples=[100], description="Rectangle width (must be > 0)")
    height: Annotated[int, Field(gt=0, strict=True)] = Field(
        examples=[200], description="Rectangle height (must be > 0)"
    )


class PolygonAnnotationCore(AnnotationCore):
    type: Literal["polygon"] = Field(examples=["polygon"], description="Polygon annotation")
    coordinates: Polygon = Field(
        examples=[[[0, 100], [100, 100], [100, 0]]],
        description="Polygon coordinates (must be >= 0)",
    )


# Post models


class PostAnnotationBase(RestrictedBaseModel):
    id: Optional[UUID4] = Field(
        default=None,
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="ID of type UUID4 (only needed in post if external Ids enabled)",
    )
    creator_id: Id = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="Creator ID")
    creator_type: DataCreatorType = Field(examples=[DataCreatorType.SCOPE], description="Creator type")


class PostPointAnnotation(PostAnnotationBase, PointAnnotationCore):
    pass


class PostLineAnnotation(PostAnnotationBase, LineAnnotationCore):
    pass


class PostArrowAnnotation(PostAnnotationBase, ArrowAnnotationCore):
    pass


class PostCircleAnnotation(PostAnnotationBase, CircleAnnotationCore):
    pass


class PostRectangleAnnotation(PostAnnotationBase, RectangleAnnotationCore):
    pass


class PostPolygonAnnotation(PostAnnotationBase, PolygonAnnotationCore):
    pass


PostAnnotation = Union[
    PostPointAnnotation,
    PostLineAnnotation,
    PostArrowAnnotation,
    PostCircleAnnotation,
    PostRectangleAnnotation,
    PostPolygonAnnotation,
]


PostAnnotationLists = Union[
    List[PostPointAnnotation],
    List[PostLineAnnotation],
    List[PostArrowAnnotation],
    List[PostCircleAnnotation],
    List[PostRectangleAnnotation],
    List[PostPolygonAnnotation],
]


class PostAnnotationList(RestrictedBaseModel):
    items: PostAnnotationLists = Field(description="List of annotations (of same type, e.g. point annotations)")


PostAnnotations = Union[PostAnnotation, PostAnnotationList]


# Full and post response models


class AnnotationBase(PostAnnotationBase):
    classes: Optional[List[Class]] = Field(
        default=None, description="List of classes assigned to annotation (if with_classes is true)"
    )
    created_at: Optional[Timestamp] = Field(
        default=None, examples=[1598611645], description="UNIX timestamp in seconds - set by server"
    )
    updated_at: Optional[Timestamp] = Field(
        default=None, examples=[1598611645], description="UNIX timestamp in seconds - set by server"
    )
    is_locked: Optional[bool] = Field(
        default=None,
        examples=["false"],
        description="Flag to mark an annotation as immutable",
    )


class PointAnnotation(AnnotationBase, PointAnnotationCore):
    pass


class LineAnnotation(AnnotationBase, LineAnnotationCore):
    pass


class ArrowAnnotation(AnnotationBase, ArrowAnnotationCore):
    pass


class CircleAnnotation(AnnotationBase, CircleAnnotationCore):
    pass


class RectangleAnnotation(AnnotationBase, RectangleAnnotationCore):
    pass


class PolygonAnnotation(AnnotationBase, PolygonAnnotationCore):
    pass


Annotation = Union[
    PointAnnotation,
    LineAnnotation,
    ArrowAnnotation,
    CircleAnnotation,
    RectangleAnnotation,
    PolygonAnnotation,
]


class AnnotationCountResponse(RestrictedBaseModel):
    item_count: ItemCount = Field(examples=[12345], description="Count of all items")


class AnnotationListResponse(AnnotationCountResponse):
    items: List[Annotation] = Field(description="List of items")


class AnnotationIdList(RestrictedBaseModel):
    annotations: List[UUID4] = Field(
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of annotation ids (type UUID4)",
    )
    low_npp_centroids: Optional[List[Point]] = Field(
        default=None,
        examples=[[[100, 200], [2000, 5000], [987, 654]]],
        description=(
            "Centroids of all annotations with higher resolution (lower npp_created / npp_viewing values) "
            "than specified by npp_viewing in the query."
        ),
    )


Annotations = Union[Annotation, AnnotationListResponse]


class AnnotationList(AnnotationListResponse):
    low_npp_centroids: Optional[List[Point]] = Field(
        default=None,
        examples=[[[100, 200], [2000, 5000], [987, 654]]],
        description=(
            "Centroids of all annotations with higher resolution (lower npp_created / npp_viewing values) "
            "than specified by npp_viewing in the query."
        ),
    )


class UniqueClassValues(RestrictedBaseModel):
    unique_class_values: Optional[List[UniqueClassValue]] = Field(
        default=None,
        examples=[
            [
                "org.empaia.my_vendor.my_app.v1.classes.non_tumor",
                "org.empaia.my_vendor.my_app.v1.classes.tumor",
                None,
            ]
        ],
        description=(
            "List of unique class values for classes assigned to annotations matching given filter criteria. "
            "IMPORTANT NOTE: Can be null, if annotations without assigned classes are returned!"
        ),
    )


class AnnotationViewerList(RestrictedBaseModel):
    annotations: List[UUID4] = Field(
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of annotation Ids",
    )
    low_npp_centroids: Optional[List[Point]] = Field(
        default=None,
        examples=[[[100, 200], [2000, 5000], [987, 654]]],
        description=(
            "Centroids of all annotations with higher resolution (lower npp_created / npp_viewing values) "
            "than specified by npp_viewing in the query."
        ),
    )


# Query models


class AnnotationUniqueClassesQuery(RestrictedBaseModel):
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
    jobs: Optional[
        Union[Annotated[List[Id], Field(min_length=1)], Annotated[List[None], Field(min_length=1, max_length=1)]]
    ] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description=(
            "List of job Ids the annotations must be locked for. "
            "IMPORTANT NOTE: Can be a list with null as single value, "
            "if annotations not locked in any job should be returned!"
        ),
    )
    types: Optional[Annotated[List[AnnotationType], Field(min_length=1)]] = Field(
        default=None,
        examples=[[AnnotationType.ARROW, AnnotationType.LINE]],
        description="List of annotation types",
    )
    viewport: Optional[Viewport] = Field(
        default=None,
        description="The viewport (only annotations within are returned)",
    )
    npp_viewing: Optional[NppViewing] = Field(
        default=None,
        examples=[[5.67, 7.89]],
        description="Resolution range in npp (nanometer per pixel) to filter annotations",
    )


class AnnotationViewerQuery(AnnotationUniqueClassesQuery):
    class_values: Optional[Annotated[List[UniqueClassValue], Field(min_length=1)]] = Field(
        default=None,
        examples=[
            [
                "org.empaia.my_vendor.my_app.v1.classes.non_tumor",
                "org.empaia.my_vendor.my_app.v1.classes.tumor",
                None,
            ]
        ],
        description=(
            "List of class values. "
            "IMPORTANT NOTE: Can be null, if annotations without assigned classes should be included!"
        ),
    )


class AnnotationQuery(AnnotationViewerQuery):
    annotations: Optional[Annotated[List[Any], Field(min_length=1)]] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of Annotation Ids (must be of type UUID4)",
    )


class AnnotationQueryPosition(RestrictedBaseModel):
    id: UUID4 = Field(examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="ID of type UUID4")
    position: Annotated[int, Field(ge=0)] = Field(
        examples=[42], description="Position of annotation in result of query (starts with 0)"
    )
