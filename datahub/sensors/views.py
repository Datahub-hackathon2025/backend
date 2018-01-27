from django.shortcuts import render, get_object_or_404
from .models import Sensor, DataPoint, Light
from .serializers import SensorSerializer, DataPointSerializer, LightSerializer
from rest_framework import routers, serializers, viewsets
from rest_framework import mixins
from rest_framework.response import Response
import datetime 
import random
import pytz
PLOT_STEP = datetime.timedelta(seconds=10)
LOCAL_TZ = pytz.timezone('Europe/Moscow')
GENERATE_POINTS_SINCE = datetime.timedelta(minutes=4)

class SensorViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    def list(self, request):
        types = self.request.query_params.get('types', None)
        if not types:
            types = ['temp', 'water', 'pollution', 'electricity', 'street_light', 'parking_lot']
        else:
            types = types.split(',')
        queryset = self.queryset.filter(sensor_type__in = types)
        serializer = SensorSerializer(queryset, many=True)
        return Response(serializer.data)


class LightViewSet(viewsets.ModelViewSet):
    queryset = Light.objects.all()
    serializer_class = LightSerializer

def generate_new_point(last_point, dt):
    point = DataPoint()
    point.datetime = dt
    point.value = last_point.value + ( random.uniform(-abs(last_point.value)*0.3, abs(last_point.value)*0.3) ) + random.uniform(-1, 1)
    point.sensor = last_point.sensor
    return point

def create_missing_points_till_now(sensor):
    now = datetime.datetime.now().replace(tzinfo=None)
    print('Cur time', now)
    last_point = DataPoint.objects.filter(sensor__pk = sensor.pk).order_by('-datetime').first()
    dt = last_point.datetime.replace(tzinfo=None)
    print('DT', dt.replace(tzinfo=None))
    dt = max(now - GENERATE_POINTS_SINCE, dt)
    print('Need to make points since', dt)
    while dt < (now - PLOT_STEP):
        dt += PLOT_STEP
        new_point = generate_new_point(last_point, dt)
        new_point.save()
        print('Created missing point', new_point.datetime)
        last_point = new_point
        


class DataPointViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):

    queryset = DataPoint.objects.all()
    serializer_class = DataPointSerializer
    def list(self, request):
        sensor_id = self.request.query_params.get('sensor', None)
        if not sensor_id:
            raise Exception("sensor id required")
        sensor = get_object_or_404(Sensor, pk=int(sensor_id))
        if not sensor:
            raise
        create_missing_points_till_now(sensor)

        queryset = self.queryset.filter(sensor__pk = sensor.id).order_by('-datetime')[:30]
        serializer = DataPointSerializer(queryset, many=True)
        return Response(serializer.data)



