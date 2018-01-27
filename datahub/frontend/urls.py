from rest_framework import routers
from .views import index
from django.urls import path, include

urlpatterns = [
    path(r'', index, name='index'),
]