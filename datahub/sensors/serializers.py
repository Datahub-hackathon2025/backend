from django.conf.urls import url, include
from .models import Sensor
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('pk', 'name', 'latitude', 'longitude')
