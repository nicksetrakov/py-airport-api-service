from datetime import datetime

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
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
    Ticket,
)


# Utility functions for creating sample instances
def sample_crew(**params):
    defaults = {"first_name": "John", "last_name": "Doe"}
    defaults.update(params)
    return Crew.objects.create(**defaults)


def sample_airplane_type(**params):
    defaults = {"name": "Boeing 737"}
    defaults.update(params)
    return AirplaneType.objects.create(**defaults)


def sample_airplane(airplane_type, **params):
    defaults = {
        "name": "Airplane 1",
        "rows": 20,
        "seats_in_row": 6,
        "airplane_type": airplane_type,
    }
    defaults.update(params)
    return Airplane.objects.create(**defaults)


def sample_country(**params):
    defaults = {"name": "Country 1"}
    defaults.update(params)
    return Country.objects.create(**defaults)


def sample_city(country, **params):
    defaults = {"name": "City 1", "country": country}
    defaults.update(params)
    return City.objects.create(**defaults)


def sample_airport(city, **params):
    defaults = {"name": "Airport 1", "closest_big_city": city}
    defaults.update(params)
    return Airport.objects.create(**defaults)


def sample_route(source, destination, **params):
    defaults = {"distance": 500}
    defaults.update(params)
    return Route.objects.create(
        source=source, destination=destination, **defaults
    )


def sample_flight(route, airplane, **params):
    defaults = {
        "departure_time": datetime.now().isoformat(),
        "arrival_time": datetime.now().isoformat(),
    }
    defaults.update(params)
    flight = Flight.objects.create(route=route, airplane=airplane, **defaults)
    flight.crew.add(sample_crew())
    return flight


def sample_ticket(flight, **params):
    defaults = {"row": 1, "seat": 1}
    defaults.update(params)
    return Ticket.objects.create(flight=flight, **defaults)


def sample_order(**params):
    order = Order.objects.create(**params)

    return order


class CrewApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "testuser", "password123", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_list_crew(self):
        sample_crew()
        sample_crew(first_name="Jane", last_name="Doe")

        url = reverse("airport:crew-list")
        res = self.client.get(url)

        crew = Crew.objects.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(2, crew.count())

    def test_create_crew(self):
        url = reverse("airport:crew-list")
        payload = {"first_name": "John", "last_name": "Doe"}
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        crew = Crew.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(crew, key))


class AirplaneTypeApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "testuser", "password123", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_list_airplane_types(self):
        sample_airplane_type()
        sample_airplane_type(name="Airbus A320")

        url = reverse("airport:airplanetype-list")
        res = self.client.get(url)

        airplane_types = AirplaneType.objects.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(2, airplane_types.count())

    def test_create_airplane_type(self):
        url = reverse("airport:airplanetype-list")
        payload = {"name": "Boeing 747"}
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        airplane_type = AirplaneType.objects.get(id=res.data["id"])
        self.assertEqual(payload["name"], airplane_type.name)


class AirplaneApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "testuser", "password123", is_staff=True
        )
        self.client.force_authenticate(self.user)
        self.airplane_type = sample_airplane_type()

    def test_list_airplanes(self):
        sample_airplane(airplane_type=self.airplane_type)
        sample_airplane(airplane_type=self.airplane_type, name="Airplane 2")

        url = reverse("airport:airplane-list")
        res = self.client.get(url)

        airplanes = Airplane.objects.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(2, airplanes.count())

    def test_create_airplane(self):
        url = reverse("airport:airplane-list")
        payload = {
            "name": "Airplane 1",
            "rows": 20,
            "seats_in_row": 6,
            "airplane_type": self.airplane_type.id,
        }
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        airplane = Airplane.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(
                payload[key],
                (
                    getattr(airplane, key)
                    if key != "airplane_type"
                    else airplane.airplane_type.id
                ),
            )


class CountryApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "testuser", "password123", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_list_countries(self):
        sample_country()
        sample_country(name="Country 2")

        url = reverse("airport:country-list")
        res = self.client.get(url)

        countries = Country.objects.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(2, countries.count())

    def test_create_country(self):
        url = reverse("airport:country-list")
        payload = {"name": "Country 1"}
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        country = Country.objects.get(id=res.data["id"])
        self.assertEqual(payload["name"], country.name)


class CityApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "testuser", "password123", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_list_cities(self):
        country = sample_country()
        sample_city(country=country)
        sample_city(name="City 2", country=country)

        url = reverse("airport:city-list")
        res = self.client.get(url)

        cities = City.objects.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(2, cities.count())

    def test_create_city(self):
        url = reverse("airport:city-list")
        payload = {"name": "City 1", "country": sample_country().id}
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        city = City.objects.get(id=res.data["id"])
        self.assertEqual(payload["name"], city.name)


class AirportApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "testuser", "password123", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_list_airports(self):
        city = sample_city(country=sample_country())
        sample_airport(city=city)
        sample_airport(name="Airport 2", city=city)

        url = reverse("airport:airport-list")
        res = self.client.get(url)

        airports = Airport.objects.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(2, airports.count())

    def test_create_airport(self):
        url = reverse("airport:airport-list")
        payload = {
            "name": "Airport 1",
            "closest_big_city": sample_city(country=sample_country()).id,
        }
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        airport = Airport.objects.get(id=res.data["id"])
        self.assertEqual(payload["name"], airport.name)


class RouteApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "testuser", "password123", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_list_routes(self):
        city = sample_city(country=sample_country())
        airport1 = sample_airport(city=city)
        airport2 = sample_airport(name="Airport 2", city=city)
        sample_route(source=airport1, destination=airport2)
        sample_route(source=airport2, destination=airport1)

        url = reverse("airport:route-list")
        res = self.client.get(url)

        routes = Route.objects.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(2, routes.count())

    def test_create_route(self):
        url = reverse("airport:route-list")
        city = sample_city(country=sample_country())
        airport1 = sample_airport(city=city)
        airport2 = sample_airport(name="Airport 2", city=city)
        payload = {
            "source": airport1.id,
            "destination": airport2.id,
            "distance": 10,
        }
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        route = Route.objects.get(id=res.data["id"])
        self.assertEqual(payload["source"], route.source.id)


class FlightApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "testuser", "password123", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_list_flights(self):
        city = sample_city(country=sample_country())
        airport1 = sample_airport(city=city)
        airport2 = sample_airport(name="Airport 2", city=city)
        route1 = sample_route(source=airport1, destination=airport2)
        route2 = sample_route(source=airport2, destination=airport1)
        airplane_type1 = sample_airplane_type()
        airplane1 = sample_airplane(airplane_type=airplane_type1)
        sample_flight(route=route1, airplane=airplane1)
        sample_flight(route=route2, airplane=airplane1)

        url = reverse("airport:flight-list")
        res = self.client.get(url)

        flights = Flight.objects.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(2, flights.count())

    def test_create_flight(self):
        url = reverse("airport:flight-list")
        airplane = sample_airplane(airplane_type=sample_airplane_type())
        airport = sample_airport(city=sample_city(country=sample_country()))
        route = sample_route(source=airport, destination=airport)
        crew = sample_crew()
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": datetime.now().isoformat(),
            "arrival_time": datetime.now().isoformat(),
            "crew": [crew.id],
        }
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        flight = Flight.objects.get(id=res.data["id"])
        self.assertEqual(payload["airplane"], flight.airplane.id)


class OrderApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "testuser", "password123", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_list_orders(self):
        city = sample_city(country=sample_country(name="Country 3"))
        airport1 = sample_airport(name="Airport 3", city=city)
        airport2 = sample_airport(name="Airport 4", city=city)
        route1 = sample_route(source=airport1, destination=airport2)
        airplane_type1 = sample_airplane_type(name="Airplane Type 2")
        airplane1 = sample_airplane(airplane_type=airplane_type1)
        flight = sample_flight(route=route1, airplane=airplane1)
        order = sample_order(user=self.user)
        sample_ticket(flight=flight, order=order)

        url = reverse("airport:order-list")
        res = self.client.get(url)

        orders = Order.objects.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(1, orders.count())

    def test_create_order(self):
        url = reverse("airport:order-list")
        country = sample_country()
        city = sample_city(country=country)
        airport = sample_airport(city=city)
        airplane = sample_airplane(airplane_type=sample_airplane_type())
        flight = sample_flight(
            route=sample_route(source=airport, destination=airport),
            airplane=airplane,
        )
        payload = {
            "tickets": [
                {"row": 11, "seat": 3, "flight": flight.id},
            ]
        }
        res = self.client.post(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(id=res.data["id"])
        self.assertEqual(
            payload["tickets"][0]["flight"], order.tickets.all()[0].flight.id
        )
