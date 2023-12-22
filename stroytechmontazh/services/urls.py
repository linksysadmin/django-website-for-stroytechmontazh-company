from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexHome.as_view(), name="index"),
    path('article/<slug:article_slug>', views.article_detail, name='article'),
    path('services/<slug:service_type_slug>', views.service_type_detail, name='service_type'),
    path('services/<slug:service_type_slug>/<slug:service_slug>', views.service_detail, name='service'),
    path('objects/<slug:object_slug>', views.object_detail, name='object_detail'),
]


