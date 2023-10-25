from django.contrib import admin
from django.views.static import serve as mediaserve
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from rest_framework import routers

from .sitemaps import *
from api_service.views import ServiceViewSet    # type: ignore


sitemaps = {
    'home': MainPage,
    'services': ServicesSitemap,
    'articles': ArticlesSitemap,
}


router = routers.DefaultRouter()
router.register(r'services', ServiceViewSet, basename='services')

urlpatterns = [
    path('enter/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('', include('services.urls')),
    path('api/v4/', include(router.urls)),
    path('api/', include('api_service.urls')),
]

handler404 = "services.views.page_not_found"


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# else:
#     urlpatterns += [
#         re_path(f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$',
#                 mediaserve, {'document_root': settings.MEDIA_ROOT}),
#         re_path(f'^{settings.STATIC_URL.lstrip("/")}(?P<path>.*)$',
#                 mediaserve, {'document_root': settings.STATIC_ROOT})
#     ]
