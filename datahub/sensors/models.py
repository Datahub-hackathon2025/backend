from django.db import models

# Create your models here.
class Sensor(models.Model):
    name = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

class DataPoint(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()
