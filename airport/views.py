from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from airport.models import Crew, AirplaneType
from airport.serializers import CrewSerializer, AirplaneTypeSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminUser,)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminUser,)
