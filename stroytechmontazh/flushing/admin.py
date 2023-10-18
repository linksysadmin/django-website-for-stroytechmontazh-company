from django.contrib import admin
from .models import *


class TypeFlushingServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


class FlushingServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'service_type', 'price', 'unit', 'is_published', 'article')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'time_create')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


admin.site.register(TypeFlushingService, TypeFlushingServiceAdmin)
admin.site.register(FlushingService, FlushingServiceAdmin)
admin.site.register(FlushingGallery)
admin.site.register(Reviews)
admin.site.register(Feedback, FeedbackAdmin)



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}  # заполнять автоматически поле slug на основе поля name
    list_display = ("id", "title", "time_create", "topic", "is_published")  # поля, которые будут отображаться в админ-панели
    # list_display_links = ("id", "title")  # поля по которым мы можем перейти на соответствующую статью
    list_filter = ("is_published", "time_create", "topic__name",)   # поля по которым можно отфильтровать
    search_fields = ("title",)  # определяет поля по которым будет производиться поиск информации


@admin.register(TopicArticle)
class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")
    list_filter = ("name",)   # поля по которым можно отфильтровать
