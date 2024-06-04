import os
import uuid

from django.db import models
from django.utils.text import slugify


class Crew(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ("last_name",)


class AirplaneType(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self) -> str | models.CharField:
        return self.name


def airplane_image_file_path(instance: "Airplane", filename: str) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/airplanes/", filename)


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType, on_delete=models.CASCADE, related_name="airplanes"
    )
    image = models.ImageField(null=True, upload_to=airplane_image_file_path)

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str | models.CharField:
        return self.name

    class Meta:
        ordering = ("airplane_type", "-capacity")


class Country(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self) -> str | models.CharField:
        return self.name

    class Meta:
        ordering = ("name",)


class City(models.Model):
    name = models.CharField(max_length=250)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="cities"
    )

    def __str__(self) -> str | models.CharField:
        return self.name

    class Meta:
        ordering = ("name",)


class Airport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    closest_big_city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, related_name="airports"
    )

    def __str__(self) -> str | models.CharField:
        return self.name

    class Meta:
        ordering = ("name",)


class Route(models.Model):
    source = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="source_routes"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="destination_routes"
    )
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source.name}-{self.destination.name}"
