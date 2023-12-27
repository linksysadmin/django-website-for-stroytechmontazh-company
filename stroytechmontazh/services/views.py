from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView

from .models import *
from .forms import ContactForm
from .utils import send_message_to_telegram


class IndexHome(FormView):
    form_class = ContactForm
    template_name = 'services/index.html'
    success_url = reverse_lazy('index')

    extra_context = {
        'objects': Object.objects.all(),
        'articles': Article.objects.all(),
        'reviews': Review.objects.all(),
    }

    def form_valid(self, form):
        user_data = form.cleaned_data
        form.save()
        messages.success(self.request, "Заявка успешно отправлена!")
        send_message_to_telegram(user_data)
        return super().form_valid(form)


def service_type_detail(request, service_type_slug):
    service_type = get_object_or_404(ServiceType, slug=service_type_slug)
    services = Service.published.filter(service_type=service_type).order_by('title')
    services_gallery = ServiceGallery.objects.filter(service=service_type)
    articles = Article.objects.filter(topic=service_type)
    reviews = Review.objects.filter(service_type=service_type)
    section_for_what = SectionForWhatService.objects.filter(service_type=service_type)
    objects = Object.objects.filter(service_type=service_type)

    context = {
        'services_gallery': services_gallery,
        'service_type': service_type,
        'services': services,
        'articles': articles,
        'section_for_what': section_for_what,
        'reviews': reviews,
        'has_subtype':  service_type.has_subtype,
        'objects':  objects,
    }

    match service_type_slug:
        case 'promyvka-sistem-otopleniya':
            template_name = 'services/flushing.html'
        case _:
            template_name = 'services/service_type.html'

    return render(request, template_name=template_name, context=context)


def service_detail(request, service_type_slug, service_slug):
    service = get_object_or_404(Service, slug=service_slug)
    service_type = ServiceType.objects.get(slug=service_type_slug)
    context = {
        'service': service,
        'service_type': service_type,
    }
    return render(request, 'services/service.html', context=context)


def article_detail(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug)
    context = {
        'article': article,
    }
    return render(request, 'services/article.html', context=context)


def object_detail(request, object_slug):
    object = get_object_or_404(Object, slug=object_slug)
    object_gallery = ObjectGallery.objects.filter(object=object).order_by('time_create')
    context = {
        'object': object,
        'object_gallery': object_gallery,
    }
    return render(request, 'services/object_detail.html', context=context)


def page_not_found(request, exception):
    return render(request, 'services/404.html', status=404)
