from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from .forms import ContactForm
from django.contrib import messages

from .telegram import send_message_to_telegram


def index(request):
    services_gallery = ServiceGallery.objects.select_related('service').all()
    articles = Article.objects.all()
    reviews = Review.objects.all()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка успешно отправлена!")
            user_data = form.cleaned_data
            send_message_to_telegram(user_data)
            return redirect('index')

    context = {
        'services_gallery': services_gallery,
        'articles': articles,
        'reviews': reviews,
    }
    return render(request, 'services/index.html', context=context)


def service_type_detail(request, service_type_slug):
    service_type = get_object_or_404(ServiceType, slug=service_type_slug)
    services = Service.published.filter(service_type=service_type).order_by('title')
    services_gallery = ServiceGallery.objects.filter(service=service_type)
    articles = Article.objects.filter(topic=service_type)
    reviews = Review.objects.filter(service_type=service_type)
    section_for_what = SectionForWhatService.objects.filter(service_type=service_type)


    context = {
        'services_gallery': services_gallery,
        'service_type': service_type,
        'services': services,
        'articles': articles,
        'section_for_what': section_for_what,
        'reviews': reviews,
        'has_subtype':  service_type.has_subtype
    }
    return render(request, 'services/service_type.html', context=context)


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



def page_not_found(request, exception):
    return render(request, 'services/404.html', status=404)
