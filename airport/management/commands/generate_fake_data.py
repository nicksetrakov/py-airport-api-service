import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from airport.models import (
    Country,
    City,
    Airport,
    AirplaneType,
    Airplane,
    Route,
    Flight,
    Ticket,
    Order,
)

fake = Faker()


class Command(BaseCommand):
    help = "Generate fake data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating fake data...")
        self.create_countries()
        self.create_cities()
        self.create_airports()
        self.create_airplane_types()
        self.create_airplanes()
        self.create_routes()
        self.create_flights()
        self.create_superuser()
        self.create_orders()
        self.stdout.write("Fake data generated successfully.")

    def create_countries(self, count=10):
        self.stdout.write("Creating countries...")
        for _ in range(count):
            Country.objects.get_or_create(name=fake.country())

    def create_cities(self, count=20):
        self.stdout.write("Creating cities...")
        countries = list(Country.objects.all())
        for _ in range(count):
            City.objects.get_or_create(
                name=fake.city(), country=random.choice(countries)
            )

    def create_airports(self, count=30):
        self.stdout.write("Creating airports...")
        cities = list(City.objects.all())
        for _ in range(count):
            Airport.objects.get_or_create(
                name=fake.city() + " Airport",
                closest_big_city=random.choice(cities),
            )

    def create_airplane_types(self, count=5):
        self.stdout.write("Creating airplane types...")
        for _ in range(count):
            AirplaneType.objects.get_or_create(name=fake.word().capitalize())

    def create_airplanes(self, count=10):
        self.stdout.write("Creating airplanes...")
        airplane_types = list(AirplaneType.objects.all())
        for _ in range(count):
            Airplane.objects.get_or_create(
                name=fake.word().capitalize()
                + " "
                + str(random.randint(100, 999)),
                rows=random.randint(20, 30),
                seats_in_row=random.randint(4, 10),
                airplane_type=random.choice(airplane_types),
            )

    def create_routes(self, count=20):
        self.stdout.write("Creating routes...")
        airports = list(Airport.objects.all())
        for _ in range(count):
            source = random.choice(airports)
            destination = random.choice(airports)
            while source == destination:
                destination = random.choice(airports)
            Route.objects.get_or_create(
                source=source,
                destination=destination,
                distance=random.randint(300, 15000),
            )

    def create_flights(self, count=50):
        self.stdout.write("Creating flights...")
        airplanes = list(Airplane.objects.all())
        routes = list(Route.objects.all())
        for _ in range(count):
            departure_time = fake.date_time_this_year()
            arrival_time = fake.date_time_between_dates(
                datetime_start=departure_time
            )
            Flight.objects.get_or_create(
                route=random.choice(routes),
                airplane=random.choice(airplanes),
                departure_time=departure_time,
                arrival_time=arrival_time,
            )

    def create_orders(self, count=20):
        self.stdout.write("Creating orders...")
        flights = list(Flight.objects.all())
        users = list(get_user_model().objects.all())
        for _ in range(count):
            order = Order.objects.create(user=random.choice(users))
            for _ in range(random.randint(1, 5)):
                flight = random.choice(flights)
                row = random.randint(1, flight.airplane.rows)
                seat = random.randint(1, flight.airplane.seats_in_row)
                Ticket.objects.get_or_create(
                    order=order, flight=flight, row=row, seat=seat
                )

    def create_superuser(self):
        email = "admin@gmail.com"
        password = "admin"
        User = get_user_model()
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=password)
            self.stdout.write("Superuser created successfully.")
        else:
            self.stdout.write("Superuser already exists.")
