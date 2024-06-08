from drf_spectacular.openapi import AutoSchema
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)
from .serializers import CrewSerializer


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
    )
