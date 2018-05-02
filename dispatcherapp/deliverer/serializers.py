from rest_framework import serializers
from .models import Website

class WebsiteSerializer(serializers.Serializer):
    class Meta:
        model = Website
        fields = ( 'id','url', 'date', 'versions' )