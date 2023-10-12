from django.db import models
from django.urls import reverse


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=1)


class TypeFlushingService(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип промывки'
        verbose_name_plural = 'Типы промывки'



class FlushingService(models.Model):
    class Status(models.IntegerChoices):
        NOT_PUBLISHED = 0, 'Не опубликовано'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    service_type = models.ForeignKey(TypeFlushingService, on_delete=models.CASCADE, verbose_name='Тип промывки')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Стоимость')
    image = models.ImageField(upload_to='service_images/', null=True, blank=True, verbose_name='Изображение')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    objects = models.Manager()
    published = PublishedModel()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('service', kwargs={'service_slug': self.slug})

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class FlushingGallery(models.Model):
    service = models.ForeignKey(TypeFlushingService, on_delete=models.CASCADE, verbose_name='Тип промывки')
    image = models.ImageField(upload_to='flushing_images/', verbose_name='Изображение')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return f'{self.image}'  # type: ignore

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['service']


class Reviews(models.Model):
    client_name = models.CharField(max_length=100, verbose_name='Имя клиента')
    text = models.TextField(verbose_name='Описание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    def __str__(self):
        return f'{self.client_name}'  # type: ignore

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['time_create']


class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя потенциального клиента')
    phone = models.CharField(max_length=16, verbose_name='Номер клиента')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    def __str__(self):
        return f'{self.name}'  # type: ignore

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = ['time_create']


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    content = models.TextField(verbose_name='Содержимое')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    topic = models.ForeignKey('TopicArticle', on_delete=models.CASCADE, verbose_name='Тематика')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    image = models.ImageField(upload_to='articles_images/', null=True, blank=True, verbose_name='Изображение')

    objects = models.Manager()
    published = PublishedModel()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'article_slug': self.slug})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['time_create']


class TopicArticle(models.Model):
    name = models.CharField(max_length=255, verbose_name='Тема')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('topic', kwargs={'topic_slug': self.slug})


    class Meta:
        verbose_name = 'Тема статьи'
        verbose_name_plural = 'Темы статей'
        ordering = ['name']



