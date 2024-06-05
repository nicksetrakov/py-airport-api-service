from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from airport.models import Crew, AirplaneType, Airplane


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name",)


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name",)


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "capacity",
            "airplane_type",
        )


class AirplaneDetailSerializer(serializers.ModelSerializer):
    airplane_type = AirplaneTypeSerializer(read_only=True)

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "airplane_type",
            "capacity",
            "image",
        )


class AirplaneImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "image")


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = StringRelatedField()
