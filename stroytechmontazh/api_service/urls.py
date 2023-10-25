from django.urls import path

from .views import *

urlpatterns = [
    path('services.xml', services_xml, name='services_xml'),
]


