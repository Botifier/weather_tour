from django.db import models


class Range(models.Model):
    start = models.FloatField()
    end = models.FloatField()


class Capital(models.Model):
    temperature = models.FloatField()
    range = models.ForeignKey("Range", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    openweather_id = models.IntegerField()