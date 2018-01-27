from django.contrib import admin
from .models import Sensor, DataPoint

class SensorAdmin(admin.ModelAdmin):
    pass

class DataPointAdmin(admin.ModelAdmin):
    pass

admin.site.register(DataPoint, DataPointAdmin)
admin.site.register(Sensor, SensorAdmin)