import requests
import datetime
import os, sys
import django

#ekb_bounds = (56.965128, 60.324427, 56.700188, 60.907979)
ekb_bounds = (56.7, 60.3, 57.0, 60.9)
sensors_link = 'http://narodmon.com/api/mapBounds?bounds={},{},{},{}&uuid=2f7dd1485da9c1928671737a4d198a27&api_key=msUdQM3ZCrZKm&lang=en&limit=50'.format(*ekb_bounds)


print(sensors_link)
json = requests.get(sensors_link).json()
print(json)
sys.path.append('datahub')
os.environ['DJANGO_SETTINGS_MODULE'] = 'datahub.settings'

django.setup()

from sensors.models import Sensor, DataPoint
sensor_type_choices = [('temp', 'temp'), ('water', 'water'), ('pollution', 'pollution'), ('electricity', 'electricity'), ('street_light', 'street_light'), ('parking_lot', 'parking_lot')]
for item in json['devices']:
    new_sensor = Sensor()
    new_sensor.name = item['name']
    new_sensor.latitude = item['lat']
    new_sensor.longitude = item['lng']
    new_sensor.sensor_type = sensor_type_choices[int(item['type']) -1][0]
    new_sensor.name = item['name'] 

    new_sensor.save()

    point = DataPoint()  
    point.value = item["value"] 
    point.datetime = datetime.datetime.now()
    point.sensor = new_sensor
    point.save()

    print('New sensor', new_sensor.name, new_sensor.latitude, new_sensor.longitude)