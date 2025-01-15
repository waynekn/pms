from rest_framework import generics

from apps.projects import models, serializers


class IndustryListView(generics.ListAPIView):
    """
    A view that returns a list of all industries in the system. This view is used by the 
    frontend to populate the industry dropdown when creating a new template.

    Attributes:
        queryset (QuerySet): A queryset containing all industries in the system.
        serializer_class (Serializer): The serializer class used to serialize the industries.
    """
    queryset = models.Industry.objects.all()
    serializer_class = serializers.IndustrySerializser
