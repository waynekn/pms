from typing import Any
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import CreateView, DetailView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from .models import Organization, OrganizationMember
from .serializers import OrganizationSerializer
from .forms import OrganizationCreateForm

# Create your views here.


class UserOrganizationListView(LoginRequiredMixin, APIView):
    """
    Displays a list of organizations that the currently authenticated user
    is a member of.
    """
    model = Organization

    def get(self, request) -> Response:
        # Get all OrganizationMember entries where the user is a member
        user_organizations = OrganizationMember.objects.filter(
            user=self.request.user)

        # Get the related Organization objects for those memberships
        organizations = Organization.objects.filter(
            organization_id__in=user_organizations.values('organization_id')
        )

        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    """
    Creates an organization, saves it to the database and adds the
    user who creates the organization to its members.
    """
    template_name = 'organizations/organization_create.html'
    form_class = OrganizationCreateForm

    def form_valid(self, form):
        # If form is valid, create the organization
        organization_name = form.cleaned_data['organization_name']
        password = form.cleaned_data['organization_password']
        admin = self.request.user
        organization_name_slug = slugify(organization_name)
        hashed_password = make_password(password)

        # Ensure the slug is unique by appending a number if necessary
        counter = 1
        while Organization.objects.filter(organization_name_slug=organization_name_slug).exists():
            organization_name_slug = f"{organization_name_slug}-{counter}"
            counter += 1

        # Create an instance without saving to the database yet
        organization = form.save(commit=False)
        organization.admin = admin
        organization.organization_name_slug = organization_name_slug
        organization.organization_password = hashed_password
        organization.save()

        # Add the admin as an organization member.
        OrganizationMember.objects.create(
            organization=organization, user=admin)

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('profile_page', kwargs={'username': self.request.user.username})


class OrganizationSearchView(LoginRequiredMixin, APIView):
    """
    Search for organizations by name.

    This view receives a POST request containing a partial or full organization name.
    It returns a list of organizations whose name contains the provided search term.
    If no organizations are found, a message indicating no results is returned.
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        organization_name_query = request.data.get(
            'organization_name_query', '')

        if not organization_name_query:
            return Response({"error": "No organization name provided"}, status=400)

        organizations = Organization.objects.filter(
            organization_name__icontains=organization_name_query)

        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)


class OrganizationDetailView(DetailView):
    model = Organization
    context_object_name = 'organization'
    slug_field = 'organization_name_slug'
    slug_url_kwarg = 'organization_name_slug'
    template_name = "organizations/organization_detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        organization = self.get_object()
        context["projects"] = organization.projects.all()
        return context
