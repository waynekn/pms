from typing import Any
from django.db import transaction
from rest_framework import generics
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProjectCreateForm
from . import models
from . import serializers
from pms.utils import camel_case_to_snake_case


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


class ProjectCreateView(LoginRequiredMixin, CreateView):
    form_class = ProjectCreateForm
    template_name = "projects/project_create.html"
    success_url = reverse_lazy('organization_detail', kwargs={
                               'organization_name_slug': ''})

    def get_form_kwargs(self):
        """Add custom keyword arguments for the form."""
        kwargs = super().get_form_kwargs()
        # Pass the 'organization_name_slug' from URL kwargs to the form
        kwargs['organization_name_slug'] = self.kwargs['organization_name_slug']
        return kwargs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs.get('organization_name_slug')
        print(context)
        print(f'slug {self.kwargs.get('organization_name_slug')}')
        return context

    @transaction.atomic
    def form_valid(self, form):
        template_id = form.cleaned_data.get('template')
        project_name = form.cleaned_data.get('project_name')
        project_name_slug = slugify(project_name)
        project = form.save(commit=False)
        project.project_name_slug = project_name_slug
        project.save()

        # add the creator as a member of the project.
        models.ProjectMember.objects.create(
            member=self.request.user, project=project)

        template = get_object_or_404(models.Template, pk=template_id)

        template_phases = template.phases.all()

        for template_phase in template_phases:
            models.ProjectPhase.objects.create(
                project=project, template_phase=template_phase)

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('organization_detail', kwargs={'organization_name_slug': self.kwargs.get('organization_name_slug')})
