from django.db import models
from django.urls import reverse


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=1)


class CompanyInfo(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название компании')
    about = models.TextField(verbose_name='Описание компании')
    location = models.CharField(default='Москва и Московская область', max_length=100, verbose_name='Местоположение')
    phone = models.CharField(max_length=16, verbose_name='Номер компании')
    email = models.EmailField(max_length=254, verbose_name='Email')
    telegram = models.CharField(max_length=100, verbose_name='Telegram')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Информация о компании'
        verbose_name_plural = 'Информация о компании'


class ServiceType(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    has_subtype = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('service_type', kwargs={'service_type_slug': self.slug})

    class Meta:
        verbose_name = 'Тип услуги'
        verbose_name_plural = 'Типы услуг'


class SubTypeService(models.Model):
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Доп. подтип'
        verbose_name_plural = 'Доп. подтипы'


class Service(models.Model):
    class Status(models.IntegerChoices):
        NOT_PUBLISHED = 0, 'Не опубликовано'
        PUBLISHED = 1, 'Опубликовано'

    UNIT = (
        ("service", "услуга"),
        ("one", "единица"),
        ("circuit", "контур"),
        ("radiator", "радиатор"),
        ("m", "м"),
        ("m2", "м²"),
        ("m3", "м³"),
        ("kvt", "кВт"),
    )

    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, verbose_name='Тип услуги')
    sub_service_type = models.ForeignKey(SubTypeService, null=True, blank=True, on_delete=models.CASCADE,
                                         verbose_name='Подтип')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Стоимость')
    discount = models.IntegerField(blank=True, null=True, verbose_name='Скидка %')
    unit = models.CharField(max_length=20, choices=UNIT, default='service', verbose_name='Единица измерения')
    image = models.ImageField(upload_to='service_images/', null=True, blank=True, verbose_name='Изображение')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    page = models.BooleanField(default=True, verbose_name='Страница')
    video_url = models.URLField(max_length=500, unique=False, null=True, blank=True, verbose_name='Video URL')

    objects = models.Manager()
    published = PublishedModel()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('service', kwargs={'service_type_slug': self.service_type.slug, 'service_slug': self.slug})

    def get_service_unit(self):
        return dict(self.UNIT).get(self.unit)  # type: ignore

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class ServiceGallery(models.Model):
    class Status(models.IntegerChoices):
        NOT_PUBLISHED = 0, 'Не опубликовано'
        PUBLISHED = 1, 'Опубликовано'

    service = models.ForeignKey(ServiceType, on_delete=models.CASCADE, verbose_name='Тип услуги')
    image = models.ImageField(upload_to='flushing_images/', verbose_name='Изображение')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    objects = models.Manager()
    published = PublishedModel()

    def __str__(self):
        return f'{self.image}'  # type: ignore

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['service']


class SectionForWhatService(models.Model):
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, verbose_name='Тип услуги')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')

    def __str__(self):
        return f'{self.title}'  # type: ignore

    class Meta:
        verbose_name = 'Секция для раздела "Почему заказывают у нас"'
        verbose_name_plural = 'Секции для раздела "Почему заказывают у нас"'
        ordering = ['service_type']


class Review(models.Model):
    client_name = models.CharField(max_length=100, verbose_name='Имя клиента')
    text = models.TextField(verbose_name='Описание')
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, null=True, blank=True)
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
    phone = models.CharField(max_length=30, verbose_name='Номер клиента')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    def __str__(self):
        return f'{self.name}'  # type: ignore

    class Meta:
        verbose_name = 'Клиенты обратной связи'
        verbose_name_plural = 'Клиенты обратной связи'
        ordering = ['time_create']


class Article(models.Model):
    class Status(models.IntegerChoices):
        NOT_PUBLISHED = 0, 'Не опубликовано'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Название')
    content = models.TextField(verbose_name='Содержимое')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    topic = models.ForeignKey(ServiceType, on_delete=models.CASCADE, verbose_name='Раздел')
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
