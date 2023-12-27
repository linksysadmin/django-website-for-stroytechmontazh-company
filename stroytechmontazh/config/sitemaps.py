from django.contrib.sitemaps import Sitemap
from services.models import *


class ServicesSitemap(Sitemap):
    def items(self):
        return Service.published.all().order_by('-title')


class ArticlesSitemap(Sitemap):
    def items(self):
        return Article.published.all().order_by('-time_create')


class ObjectsSitemap(Sitemap):
    def items(self):
        return Object.published.all().order_by('-date')


class MainPage(Sitemap):
    def items(self):
        return ['index']

    def location(self, item):
        return reverse('index')