from django.shortcuts import render
from .models import Sensor, DataPoint, Light
from .serializers import SensorSerializer, DataPointSerializer, LightSerializer
from rest_framework import routers, serializers, viewsets
from rest_framework import mixins
from rest_framework.response import Response
import datetime 
import random
class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class LightViewSet(viewsets.ModelViewSet):
    queryset = Light.objects.all()
    serializer_class = LightSerializer

def generate_new_point(last_point):
    point = DataPoint()
    point.datetime = last_point.datetime + datetime.timedelta(seconds=2)
    point.value = last_point.value + random.uniform(last_point.value - last_point.value*0.5, last_point.value+last_point.value*0.5) * random.choice([-1, 1, 0])
    point.sensor = last_point.sensor
    return point

class DataPointViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):

    queryset = DataPoint.objects.all()
    serializer_class = DataPointSerializer
    def list(self, request):
        sensor = self.request.query_params.get('sensor', None)
        if not sensor:
            raise Exception("sensor id required")

        last_point = self.queryset.filter(sensor__pk = sensor).order_by('-datetime').first()
        new_point = generate_new_point(last_point)
        new_point.save()

        queryset = self.queryset.filter(sensor__pk = sensor)
        serializer = DataPointSerializer(queryset, many=True)
        return Response(serializer.data)



