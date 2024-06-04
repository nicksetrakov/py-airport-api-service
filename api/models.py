from django.db import models


class Crew(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ("last_name",)
