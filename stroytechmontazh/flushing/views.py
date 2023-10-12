from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import ContactForm
from django.contrib import messages

from .telegram import send_message_to_telegram


def index(request):
    flushing_type = TypeFlushingService.objects.all()
    flushing_galleries = FlushingGallery.objects.select_related('service').all()
    reviews = Reviews.objects.all()
    articles = Article.objects.all()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка успешно отправлена!")
            user_data = form.cleaned_data
            send_message_to_telegram(user_data)
            return redirect('index')

    context = {
        'flushing_types': flushing_type,
        'flushing_galleries': flushing_galleries,
        'reviews': reviews,
        'articles': articles,
    }
    return render(request, 'flushing/index.html', context=context)


def service_detail(request, service_slug):
    service = get_object_or_404(FlushingService, slug=service_slug)
    context = {
        'service': service,
    }
    return render(request, 'flushing/service.html', context=context)


def article_detail(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug)
    context = {
        'article': article,
    }
    return render(request, 'flushing/article.html', context=context)


def topic_detail(request, topic_slug):
    topic = get_object_or_404(TopicArticle, slug=topic_slug)
    articles = Article.objects.filter(topic=topic, is_published=True)
    context = {
        'topic': topic,
        'articles': articles,
    }
    return render(request, 'flushing/topic.html', context=context)

