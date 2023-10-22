from .forms import ContactForm
from .models import Service, ServiceType, CompanyInfo, Review


def contact_form(request):
    return {'contact_form': ContactForm()}


def services_types(request):
    return {'services_types': ServiceType.objects.all()}


def company_info(request):
    return {'company_info': CompanyInfo.objects.first()}


