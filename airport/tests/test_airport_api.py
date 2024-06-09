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
        "departure_time": "2024-06-10 08:00:00",
        "arrival_time": "2024-06-10 12:00:00",
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
    order.tickets.add(
        sample_ticket(
            flight=sample_flight(
                route=sample_route(
                    source=sample_airport(
                        city=sample_city(country=sample_country())
                    ),
                    destination=sample_airport(
                        city=sample_city(country=sample_country())
                    ),
                ),
                airplane=sample_airplane(airplane_type=sample_airplane_type()),
            )
        )
    )
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
        sample_country()
        sample_country(name="City 2")

        url = reverse("airport:city-list")
        res = self.client.get(url)

        countries = Country.objects.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(2, countries.count())

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

    def test_list_cities(self):
        sample_country()
        sample_country(name="City 2")

        url = reverse("airport:city-list")
        res = self.client.get(url)

        countries = Country.objects.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(2, countries.count())

    def test_create_city(self):
        url = reverse("airport:city-list")
        payload = {"name": "City 1", "country": sample_country().id}
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        city = City.objects.get(id=res.data["id"])
        self.assertEqual(payload["name"], city.name)
