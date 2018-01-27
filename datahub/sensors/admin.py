from django.contrib import admin
from .models import Sensor, DataPoint, Light

class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'sensor_type')

class LightAdmin(admin.ModelAdmin):
    list_display = ('name', 'state_on')

class DataPointAdmin(admin.ModelAdmin):
    list_display = ('datetime','value','sensor')

admin.site.register(DataPoint, DataPointAdmin)
admin.site.register(Light, LightAdmin)
admin.site.register(Sensor, SensorAdmin)