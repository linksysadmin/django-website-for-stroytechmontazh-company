from .forms import ContactForm
from .models import FlushingService, TopicArticle


def contact_form(request):
    return {'contact_form': ContactForm()}


def services(request):
    return {'services': FlushingService.published.order_by('title')}


def topics(request):
    return {'topics':  TopicArticle.objects.all()}  # type: ignore


