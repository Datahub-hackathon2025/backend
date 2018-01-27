from django.db import models

# Create your models here.
class Sensor(models.Model):
    name = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    sensor_type = models.CharField(max_length=50, choices=(('temp', 'temp'), ('pollution', 'pollution'), ('electricity', 'electricity'), ('street_light', 'street_light'), ('parking_lot', 'parking_lot')))

class Light(Sensor):
    state_on = models.BooleanField()

class ParkingLot(Sensor):
    state_free = models.BooleanField()

class DataPoint(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()
    datetime = models.DateTimeField()
