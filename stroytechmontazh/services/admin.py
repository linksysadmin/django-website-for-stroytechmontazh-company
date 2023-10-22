from django.contrib import admin
from .models import *


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'telegram')
    list_display_links = ('id', 'name')


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(SubTypeService)
class SubTypeServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'sub_service_type', 'price', 'unit', 'is_published', 'page')
    list_display_links = ('id', 'title')
    list_filter = ("is_published", "service_type", "page", 'price')  # поля по которым можно отфильтровать
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'time_create')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(ServiceGallery)
class ServiceGalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'is_published', 'time_create')
    list_display_links = ('id', 'service')
    search_fields = ('service',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}  # заполнять автоматически поле slug на основе поля name
    list_display = (
        "id", "title", "time_create", "topic", "is_published")  # поля, которые будут отображаться в админ-панели
    list_display_links = ("id", "title")  # поля по которым мы можем перейти на соответствующую статью
    list_filter = ("is_published", "time_create", "topic__title",)  # поля по которым можно отфильтровать
    search_fields = ("title",)  # определяет поля по которым будет производиться поиск информации


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("client_name", "text", "time_create")
    list_filter = ("client_name", "time_create", )  # поля по которым можно отфильтровать


@admin.register(SectionForWhatService)
class SectionForWhatServiceAdmin(admin.ModelAdmin):
    list_display = ("service_type", "title",)
    list_filter = ("service_type", "title", )  # поля по которым можно отфильтровать
