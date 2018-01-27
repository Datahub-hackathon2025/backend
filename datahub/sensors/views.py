from django.shortcuts import render
from .models import Sensor
from .serializers import SensorSerializer
from rest_framework import routers, serializers, viewsets

# ViewSets define the view behavior.
class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer