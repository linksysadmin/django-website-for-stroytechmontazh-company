from django.urls import path
from django.views.decorators.cache import cache_page

from . import views



urlpatterns = [
    path('', views.index, name="index"),
    path('service/<slug:service_slug>', views.service_detail, name='service'),
    path('article/<slug:article_slug>', views.article_detail, name='article'),
    path('topic/<slug:topic_slug>', views.topic_detail, name='topic'),

    # path('', cache_page(60)(views.index), name='index'),
]


