from django.db.models import Count, F, ExpressionWrapper, IntegerField
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from airport.filters import FlightFilter
from airport.models import (
    Crew,
    AirplaneType,
    Airplane,
    Country,
    City,
    Airport,
    Route,
    Flight,
    Order,
)
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.schemas import (
    CrewSchema,
    AirplaneTypeSchema,
    AirplaneSchema,
    CountrySchema,
    CitySchema,
    AirportSchema,
    RouteSchema,
    FlightSchema,
    OrderSchema,
)
from airport.serializers import (
    CrewSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirplaneListSerializer,
    AirplaneDetailSerializer,
    AirplaneImageSerializer,
    CountrySerializer,
    CitySerializer,
    CityListSerializer,
    CityDetailSerializer,
    AirportSerializer,
    AirportDetailSerializer,
    AirportListSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    FlightSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    OrderSerializer,
    OrderListSerializer,
    OrderDetailSerializer,
)


@extend_schema_view(list=CrewSchema.list)
class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["first_name", "last_name"]
    search_fields = ["first_name", "last_name"]
    permission_classes = [
        IsAdminUser,
    ]


@extend_schema_view(list=AirplaneTypeSchema.list)
class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["name"]
    search_fields = ["name"]
    permission_classes = [
        IsAdminUser,
    ]


@extend_schema_view(
    list=AirplaneSchema.list,
    retrieve=AirplaneSchema.retrieve,
)
class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = ["name", "airplane_capacity", "airplane_type"]
    search_fields = ["name", "airplane_type__name"]
    filterset_fields = ["airplane_type__name"]
    permission_classes = [
        IsAdminOrIfAuthenticatedReadOnly,
    ]

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = queryset.annotate(
                airplane_capacity=ExpressionWrapper(
                    F("rows") * F("seats_in_row"), output_field=IntegerField()
                )
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer

        if self.action == "retrieve":
            return AirplaneDetailSerializer

        if self.action == "upload_image":
            return AirplaneImageSerializer

        return self.serializer_class

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        item = self.get_object()
        serializer = self.get_serializer(item, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=CountrySchema.list,
)
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["name"]
    search_fields = ["name"]
    permission_classes = [
        IsAdminUser,
    ]


@extend_schema_view(
    list=CitySchema.list,
    retrieve=CitySchema.retrieve,
)
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related("country")
    serializer_class = CitySerializer
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = ["name", "country"]
    search_fields = ["name"]
    filterset_fields = ["country__name"]
    permission_classes = [
        IsAdminUser,
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return CityListSerializer

        if self.action == "retrieve":
            return CityDetailSerializer

        return self.serializer_class


@extend_schema_view(
    list=AirportSchema.list,
    retrieve=AirportSchema.retrieve,
)
class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.select_related(
        "closest_big_city__country",
    )
    serializer_class = AirportSerializer
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = [
        "name",
        "closest_big_city__name",
        "closest_big_city__country",
    ]
    search_fields = [
        "name",
        "closest_big_city__name",
        "closest_big_city__country__name",
    ]
    filterset_fields = [
        "closest_big_city__name",
        "closest_big_city__country__name",
    ]
    permission_classes = [
        IsAdminOrIfAuthenticatedReadOnly,
    ]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AirportDetailSerializer
        if self.action == "list":
            return AirportListSerializer

        return super().get_serializer_class()


@extend_schema_view(
    list=RouteSchema.list,
    retrieve=RouteSchema.retrieve,
)
class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related(
        "source__closest_big_city__country",
        "destination__closest_big_city__country",
    )
    serializer_class = RouteSerializer
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = ["source", "destination"]
    search_fields = [
        "source__name",
        "source__closest_big_city__name",
        "source__closest_big_city__country__name",
    ]
    filterset_fields = [
        "source__name",
        "source__closest_big_city__name",
        "source__closest_big_city__country__name",
    ]
    permission_classes = [
        IsAdminOrIfAuthenticatedReadOnly,
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer

        if self.action == "retrieve":
            return RouteDetailSerializer

        return super().get_serializer_class()


@extend_schema_view(
    list=FlightSchema.list,
    retrieve=FlightSchema.retrieve,
)
class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related(
        "route__source__closest_big_city__country",
        "route__destination__closest_big_city__country",
        "airplane__airplane_type",
    ).prefetch_related("crew")
    serializer_class = FlightSerializer
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = ["departure_time", "arrival_time"]
    search_fields = [
        "route__source__name",
        "route__source__closest_big_city__name",
        "route__source__closest_big_city__country__name",
    ]
    filterset_class = FlightFilter
    permission_classes = [
        IsAdminOrIfAuthenticatedReadOnly,
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action in ("list", "retrieve"):
            queryset = queryset.annotate(
                tickets_available=F("airplane__rows")
                * F("airplane__seats_in_row")
                - Count("tickets")
            )
        return queryset

    def get_serializer_class(self):

        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        return super().get_serializer_class()

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 60 * 2))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@extend_schema_view(
    list=OrderSchema.list,
    retrieve=OrderSchema.retrieve,
)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related(
        "tickets__flight__route__source__closest_big_city__country",
        "tickets__flight__route__destination__closest_big_city__country",
        "tickets__flight__crew",
        "tickets__flight__airplane__airplane_type",
    )
    serializer_class = OrderSerializer
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = [
        "created_at",
        "tickets__flight__departure_time",
        "tickets__flight__arrival_time",
    ]
    search_fields = [
        "tickets__flight__route__source__name",
        "tickets__flight__route__source__closest_big_city__name",
        "tickets__flight__route__source__closest_big_city__country__name",
    ]
    filterset_fields = [
        "tickets__flight__route__source__name",
        "tickets__flight__route__source__closest_big_city__name",
        "tickets__flight__route__source__closest_big_city__country__name",
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).distinct()

    def get_permissions(self):
        if self.action in (
            "update",
            "partial_update",
        ):
            return [
                IsAdminUser(),
            ]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        if self.action == "retrieve":
            return OrderDetailSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
