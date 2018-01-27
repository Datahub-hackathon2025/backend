from django.shortcuts import render
from .models import Sensor, DataPoint, Light
from .serializers import SensorSerializer, DataPointSerializer, LightSerializer
from rest_framework import routers, serializers, viewsets
from rest_framework import mixins
from rest_framework.response import Response

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class LightViewSet(viewsets.ModelViewSet):
    queryset = Light.objects.all()
    serializer_class = LightSerializer

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
        queryset = self.queryset.filter(sensor__pk = sensor)
        serializer = DataPointSerializer(queryset, many=True)
        return Response(serializer.data)



