from django.urls import path, include
from rest_framework import routers

from airport.views import (
    CrewViewSet, AirplaneTypeViewSet, AirplaneViewSet, CountryViewSet,
)

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("airplane-types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("countries", CountryViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "airport"
