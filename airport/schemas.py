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
    CountrySerializer,
    CityListSerializer,
    CityDetailSerializer,
    AirportListSerializer,
    AirportDetailSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
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
            OpenApiParameter(
                name="airplane_type__name",
                description="Filter by airplane type name (ex. ?airplane_type__name=Boeing 747)",
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


class CountrySchema:
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
                description="Search by name (ex. ?search=Ukraine)",
                required=False,
                type=OpenApiTypes.STR,
            ),
        ],
        responses={
            200: CountrySerializer(many=True),
        },
    )


class CitySchema:
    list = extend_schema(
        parameters=[
            OpenApiParameter(
                name="ordering",
                description="Order by name, country (ex. ?ordering=name,-country)",
                required=False,
                type={"type": "array", "items": {"type": "string"}},
                style="form",
                explode=False,
            ),
            OpenApiParameter(
                name="search",
                description="Search by name (ex. ?search=Kiev)",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="country__name",
                description="Filter by country name (ex. ?country__name=Ukraine)",
                required=False,
                type=OpenApiTypes.STR,
            ),
        ],
        responses={
            200: CityListSerializer(many=True),
        },
    )
    retrieve = extend_schema(
        responses={
            200: CityDetailSerializer,
        }
    )


class AirportSchema:
    list = extend_schema(
        parameters=[
            OpenApiParameter(
                name="ordering",
                description=(
                    "Order by name, closest_big_city__name, closest_big_city__country "
                    "(ex. ?ordering=name,-closest_big_city__country)"
                ),
                required=False,
                type={"type": "array", "items": {"type": "string"}},
                style="form",
                explode=False,
            ),
            OpenApiParameter(
                name="search",
                description=(
                    "Search by name, city name, country name (ex. ?search=Kiev)"
                ),
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="closest_big_city__name",
                description="Filter by closest_big_city__name (ex. ?closest_big_city__name=Kiev)",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="closest_big_city__country__name",
                description="Filter by closest_big_city__country__name (ex. ?closest_big_city__country__name=Ukraine)",
                required=False,
                type=OpenApiTypes.STR,
            ),
        ],
        responses={
            200: AirportListSerializer(many=True),
        },
    )
    retrieve = extend_schema(
        responses={
            200: AirportDetailSerializer,
        }
    )


class RouteSchema:
    list = extend_schema(
        parameters=[
            OpenApiParameter(
                name="ordering",
                description=(
                    "Order by source, destination" "(ex. ?ordering=source,-destination)"
                ),
                required=False,
                type={"type": "array", "items": {"type": "string"}},
                style="form",
                explode=False,
            ),
            OpenApiParameter(
                name="search",
                description=(
                    "Search by source name, city name and country name "
                    "(ex. ?search=Kiev)"
                ),
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="source__name",
                description=(
                    "Filter by source__name "
                    "(ex. ?source__name=Borispil)"
                ),
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="source__closest_big_city__name",
                description=(
                    "Filter by source__closest_big_city__name "
                    "(ex. ?source__closest_big_city__name=Kiev)"
                ),
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="source__closest_big_city__country__name",
                description=(
                    "Filter by source__closest_big_city__country__name "
                    "(ex. ?source__closest_big_city__country__name=Ukraine)"
                ),
                required=False,
                type=OpenApiTypes.STR,
            ),
        ],
        responses={
            200: RouteListSerializer(many=True),
        },
    )
    retrieve = extend_schema(
        responses={
            200: RouteDetailSerializer,
        }
    )
