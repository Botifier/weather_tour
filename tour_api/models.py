from django.db import models
from .enums import DestinationTypes


class Package(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    description = models.TextField()
    destination = models.ManyToManyField("Destination")


class Tour(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    capacity = models.IntegerField()
    package = models.ForeignKey("Package", on_delete=models.CASCADE)


class Destination(models.Model):
    city = models.CharField(unique=True, max_length=50)
    destination_type = models.CharField(
      max_length = 10,
      choices=[(type_, type_.value) for type_ in DestinationTypes]
    )
    danger_score = models.FloatField()