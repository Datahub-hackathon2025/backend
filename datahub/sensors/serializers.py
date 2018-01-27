from django.conf.urls import url, include
from .models import Sensor, Light, DataPoint
from rest_framework import routers, serializers, viewsets

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('pk', 'name', 'latitude', 'longitude', 'sensor_type')

class LightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Light
        fields = ('pk', 'name', 'latitude', 'longitude', 'sensor_type', 'state_on')

class DataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        fields = ('value', 'datetime')
