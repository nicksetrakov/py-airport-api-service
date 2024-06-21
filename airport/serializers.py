from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from airport.models import (
    Crew,
    AirplaneType,
    Airplane,
    Country,
    City,
    Route,
    Airport,
    Flight,
    Ticket,
    Order,
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
    tickets_available = serializers.IntegerField()
    airplane = serializers.StringRelatedField()
    crew = serializers.StringRelatedField(many=True)
    departure_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )
    arrival_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "tickets_available",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane,
            ValidationError,
        )
        return data

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "flight",
        )


class TicketSeatSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class FlightDetailSerializer(FlightListSerializer):
    route = RouteDetailSerializer()
    taken_places = TicketSeatSerializer(
        source="tickets", many=True, read_only=True
    )
    airplane = AirplaneDetailSerializer()
    crew = CrewSerializer(many=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "taken_places",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
        )


class TicketListSerializer(TicketSerializer):
    flight = serializers.StringRelatedField()


class TicketDetailSerializer(TicketSerializer):
    flight = FlightDetailSerializer()


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    @transaction.atomic()
    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        order = Order.objects.create(**validated_data)
        for ticket_data in tickets_data:
            Ticket.objects.create(order=order, **ticket_data)
        return order


class OrderListSerializer(OrderSerializer):
    tickets = serializers.StringRelatedField(many=True)


class OrderDetailSerializer(OrderSerializer):
    tickets = TicketDetailSerializer(many=True)
