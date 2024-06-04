from django.urls import path, include
from rest_framework import routers

from airport.views import (
    CrewViewSet, AirplaneTypeViewSet,
)

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("airplane-types", AirplaneTypeViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "airport"
