from django.contrib import admin

from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import *
from django.views.static import serve as mediaserve

sitemaps = {
    'services': ServicesSitemap,
    'articles': ArticlesSitemap,
    'topic_articles': TopicArticleSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('', include('flushing.urls')),
]


if settings.DEBUG:
    # import debug_toolbar

    # urlpatterns = [
    #                   path('__debug__/', include(debug_toolbar.urls)),
    #               ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# else:
#     urlpatterns += [
#         re_path(f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$',
#                 mediaserve, {'document_root': settings.MEDIA_ROOT}),
#         re_path(f'^{settings.STATIC_URL.lstrip("/")}(?P<path>.*)$',
#                 mediaserve, {'document_root': settings.STATIC_ROOT})
#     ]
