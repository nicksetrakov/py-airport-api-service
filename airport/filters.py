import django_filters
from django_filters import rest_framework as filters

from airport.models import Flight


class FlightFilter(filters.FilterSet):
    departure_time = django_filters.DateFromToRangeFilter()
    arrival_time = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Flight
        fields = [
            "route__source__name",
            "route__destination__name",
            "route__source__closest_big_city__name",
            "route__destination__closest_big_city__name",
            "route__source__closest_big_city__country__name",
            "route__destination__closest_big_city__country__name",
            "departure_time",
            "arrival_time",
        ]
