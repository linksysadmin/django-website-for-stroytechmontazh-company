from django.contrib.sitemaps import Sitemap
from services.models import *


class ServicesSitemap(Sitemap):
    def items(self):
        return Service.published.all()


class ArticlesSitemap(Sitemap):
    def items(self):
        return Article.published.all()


class MainPage(Sitemap):
    def items(self):
        return ['index']

    def location(self, item):
        return reverse('index')
