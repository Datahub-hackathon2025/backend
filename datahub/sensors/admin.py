from django.contrib import admin
from .models import Sensor

class SensorAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Sensor, SensorAdmin)