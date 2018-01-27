from django.shortcuts import render, get_object_or_404
from .models import Sensor, DataPoint, Light
from .serializers import SensorSerializer, DataPointSerializer, LightSerializer
from rest_framework import routers, serializers, viewsets
from rest_framework import mixins
from rest_framework.response import Response
import datetime 
import random
import pytz
PLOT_STEP = datetime.timedelta(seconds=5)
LOCAL_TZ = pytz.timezone('Europe/Moscow')
GENERATE_POINTS_SINCE = datetime.timedelta(minutes=2)

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

def generate_new_point(last_point, dt, sensor_type):
    point = DataPoint()
    point.datetime = dt

    old_val = last_point.value
    random_walk = random.uniform(-abs(old_val)*0.3, abs(old_val)*0.3)
    noise = random.uniform(-old_val*0.05, old_val*0.05)

    if (sensor_type == 'pollution'):
        random_walk = random.uniform(-abs(old_val)*0.05, abs(old_val)*0.05)
        noise = random.uniform(-old_val*0.02, old_val*0.02)

    if old_val == 0:
        noise = random.uniform(-1, 1)

    print(old_val, random_walk, noise, old_val + random_walk + noise)
    point.value =  old_val + random_walk + noise
    
    if (sensor_type == 'temp'):
        point.value = max(min(point.value, -10), -30)
    else:
        point.value = max(min(point.value, 100), 0)

    point.sensor = last_point.sensor
    return point

def create_missing_points_till_now(sensor):
    now = datetime.datetime.now().replace(tzinfo=None)
    print('Cur time', now)
    last_point = DataPoint.objects.filter(sensor__pk = sensor.pk).order_by('-datetime').first()
    if last_point:
        dt = last_point.datetime.astimezone(LOCAL_TZ).replace(tzinfo=None) + PLOT_STEP
        print('DT', dt)
        dt = max(now - GENERATE_POINTS_SINCE, dt)
        print('Need to make points since', dt, 'till', (now - PLOT_STEP))
        while dt < (now - PLOT_STEP):
            new_point = generate_new_point(last_point, dt, sensor.sensor_type)
            new_point.save()
            print('Created missing point', new_point.datetime)
            last_point = new_point
            dt += PLOT_STEP
    else:

        point = DataPoint()
        point.sensor = sensor
        point.datetime = now
        point.value = random.uniform(0, 100)
        point.save()
        print('Created initial point', point.datetime)

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



