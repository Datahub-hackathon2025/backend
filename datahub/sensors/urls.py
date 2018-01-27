from rest_framework import routers
from .views import SensorViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'sensors', SensorViewSet)
router.register(r'sensors', SensorViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]