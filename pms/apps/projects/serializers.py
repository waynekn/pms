from rest_framework import serializers
from . import models


class IndustrySerializser(serializers.ModelSerializer):
    """
    A serializer class for the `Industry` model. This class is used by the API to serialize 
    `Industry` instances into JSON data before returning it to the client.

    Attributes:
        Meta (class): A class containing metadata for the serializer.
    """
    class Meta:
        model = models.Industry
        fields = ['industry_id', 'industry_name']
