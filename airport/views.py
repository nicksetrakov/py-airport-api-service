from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from airport.models import Crew, AirplaneType, Airplane, Country, City, Airport, Route
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
)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminUser,)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminUser,)


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminUser,)

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [
                IsAuthenticated(),
            ]
        if self.action in (
            "create",
            "update",
            "partial_update",
            "upload_image",
            "destroy",
        ):
            return [
                IsAdminUser(),
            ]

        return super().get_permissions()

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


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsAdminUser,)


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related("country")
    serializer_class = CitySerializer
    permission_classes = (IsAdminUser,)

    def get_serializer_class(self):
        if self.action == "list":
            return CityListSerializer

        if self.action == "retrieve":
            return CityDetailSerializer

        return self.serializer_class


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.select_related(
        "closest_big_city__country",
    )
    serializer_class = AirportSerializer
    permission_classes = (IsAdminUser,)

    def get_permissions(self):

        if self.action in ("list", "retrieve"):
            return [
                IsAuthenticated(),
            ]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AirportDetailSerializer
        if self.action == "list":
            return AirportListSerializer

        return super().get_serializer_class()


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related(
        "source__closest_big_city__country",
        "destination__closest_big_city__country",
    )
    serializer_class = RouteSerializer

    def get_permissions(self):

        if self.action in ("list", "retrieve"):
            return [
                IsAuthenticated(),
            ]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer

        if self.action == "retrieve":
            return RouteDetailSerializer

        return super().get_serializer_class()
