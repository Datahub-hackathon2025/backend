from rest_framework import routers
from .views import SensorViewSet, DataPointViewSet, LightViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'sensors', SensorViewSet)
router.register(r'points', DataPointViewSet)
router.register(r'lights', LightViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]