from rest_framework import serializers

from airport.models import (
    Crew,
    AirplaneType,
    Airplane,
    Country,
    City,
    Route,
    Airport,
    Flight,
)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = (
            "id",
            "first_name",
            "last_name",
        )


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = (
            "id",
            "name",
        )


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
    airplane_type = serializers.StringRelatedField()


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "country")


class CityListSerializer(CitySerializer):
    country = serializers.StringRelatedField()


class CityDetailSerializer(CitySerializer):
    country = CountrySerializer()


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = (
            "id",
            "name",
            "closest_big_city",
        )


class AirportListSerializer(AirportSerializer):
    closest_big_city = serializers.StringRelatedField()


class AirportDetailSerializer(AirportSerializer):
    closest_big_city = CityDetailSerializer()


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = (
            "id",
            "source",
            "destination",
            "distance",
        )


class RouteListSerializer(RouteSerializer):
    source = serializers.StringRelatedField()
    destination = serializers.StringRelatedField()


class RouteDetailSerializer(RouteSerializer):
    destination = AirportDetailSerializer()
    source = AirportDetailSerializer()


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
        )


class FlightListSerializer(FlightSerializer):
    route = serializers.StringRelatedField()
    airplane = serializers.StringRelatedField()
    crew = serializers.StringRelatedField(many=True)
    departure_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )
    arrival_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
        )


class FlightDetailSerializer(FlightListSerializer):
    route = RouteDetailSerializer()
    airplane = AirplaneDetailSerializer()
    crew = CrewSerializer(many=True)
    count_free_seats = serializers.IntegerField(source="free_tickets_seat")

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
            "count_free_seats",
        )
