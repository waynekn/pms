from rest_framework import generics

from rest_framework import generics
from rest_framework import status

from rest_framework.response import Response

from pms.utils import camel_case_to_snake_case
from apps.projects import models, serializers


class TemplateCreateView(generics.CreateAPIView):
    """
    A view to handle the creation of a new Template resource.

    This view accepts a POST request with the data for a new template, processes
    the `TemplateCreateForm` data (transformed to snake_case), and creates a 
    `Template` instance along with its associated `TemplatePhase` instances. 
    If the form is valid, the new template and phases are saved to the database 
    and a successful response with the created template data is returned. 
    If the form is invalid, a 400 Bad Request response with errors is returned.

    Attributes:
        model (class): The model associated with this view, `Template`.
        serializer_class (class): The serializer class used for serializing
                                  template data, `TemplateSerializer`.

    """
    model = models.Template
    serializer_class = serializers.TemplateSerializer

    def post(self, request, *args, **kwargs):
        transformed_data = camel_case_to_snake_case(request.data)
        serializer = self.get_serializer(
            data=transformed_data, context={'request': request, 'template_phases': transformed_data.get('template_phases')})

        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateSearchView(generics.ListAPIView):
    """
    Handles searching for a template by name.
    """

    serializer_class = serializers.TemplateSearchSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name')
        name = name.strip() if name else None

        if not name:
            return []

        return models.Template.objects.filter(
            template_name__icontains=name)
