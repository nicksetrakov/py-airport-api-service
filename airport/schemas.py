from drf_spectacular.openapi import AutoSchema
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)
from .serializers import (
    CrewSerializer,
    AirplaneTypeSerializer,
    AirplaneImageSerializer,
    AirplaneDetailSerializer,
    AirplaneListSerializer,
)


class CrewSchema:
    list = extend_schema(
        parameters=[
            OpenApiParameter(
                name="ordering",
                description="Order by first_name or last_name (ex. ?ordering=first_name,last_name)",
                required=False,
                type={"type": "array", "items": {"type": "string"}},
                style="form",
                explode=False,
            ),
            OpenApiParameter(
                name="search",
                description="Search by first_name or last_name (ex. ?search=David)",
                required=False,
                type=OpenApiTypes.STR,
            ),
        ],
        responses={
            200: CrewSerializer(many=True),
        },
    )


class AirplaneTypeSchema:
    list = extend_schema(
        parameters=[
            OpenApiParameter(
                name="ordering",
                description="Order by name (ex. ?ordering=name)",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="search",
                description="Search by name (ex. ?search=Boeing)",
                required=False,
                type=OpenApiTypes.STR,
            ),
        ],
        responses={
            200: AirplaneTypeSerializer(many=True),
        },
    )


class AirplaneSchema:
    list = extend_schema(
        parameters=[
            OpenApiParameter(
                name="ordering",
                description="Order by name, airplane_capacity, or airplane_type (ex. ?ordering=name,-airplane_capacity)",
                required=False,
                type={"type": "array", "items": {"type": "string"}},
                style="form",
                explode=False,
            ),
            OpenApiParameter(
                name="search",
                description="Search by name or airplane type name (ex. ?search=Boeing)",
                required=False,
                type=OpenApiTypes.STR,
            ),
        ],
        responses={
            200: AirplaneListSerializer(many=True),
        },
    )

    retrieve = extend_schema(
        responses={
            200: AirplaneDetailSerializer,
        }
    )
