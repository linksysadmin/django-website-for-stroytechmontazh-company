from django.http import HttpResponse
from rest_framework import viewsets  # Базовые классы для представления

from .serializers import ServiceSerializer
from services.models import Service, ServiceType, SubTypeService, CompanyInfo  # type: ignore

from .xml import generate_xml


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.published.all().order_by('title')
    serializer_class = ServiceSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


def services_xml(request):
    data = {
        'company_info': CompanyInfo.objects.get(pk=1),
        'services': Service.published.all(),
        'main_categories': ServiceType.objects.all(),
        'sub_categories': SubTypeService.objects.all(),
    }
    xml_string = generate_xml(request, data)
    response = HttpResponse(xml_string, content_type='application/xml')
    return response
