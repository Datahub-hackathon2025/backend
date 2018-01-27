from django.conf.urls import url, include
from .models import Sensor, Light, DataPoint
from rest_framework import routers, serializers, viewsets


class LightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Light
        fields = ('pk', 'name', 'latitude', 'longitude', 'state_on')

class DataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        fields = ('value', 'datetime')

class SensorSerializer(serializers.ModelSerializer):
    current_value = DataPointSerializer(many=False, read_only=True)
    #datapoints = serializers.StringRelatedField(many=True)
    class Meta:
        model = Sensor
        fields = ('pk', 'name', 'latitude', 'longitude', 'sensor_type', 'current_value')
