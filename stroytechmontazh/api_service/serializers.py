from rest_framework import serializers

from services.models import Service, SubTypeService, ServiceType   # type: ignore


class ServiceSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['title', 'service_type', 'sub_service_type', 'description', 'price', 'image', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.get_absolute_url())
        return None
