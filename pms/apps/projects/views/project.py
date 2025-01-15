from uuid import UUID

from rest_framework import status
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response

from pms.utils import camel_case_to_snake_case

from apps.projects import models, serializers
from apps.organizations.models import OrganizationMember


class ProjectCreateView(generics.CreateAPIView):
    """
    A view that handles the creation of a new project.

    This view accets a POST request with the data with the following data necessary
    to create a project: 
    - organization,project name, template(optional), description and deadline

    Upon successful validation, the new project instance is created, and a `201 Created` 
    response with the serialized data of the project is returned.
    If validation fails, a `400 Bad Request` response with error details is returned.

    Attributes:
        model (models.Project): The model associated with this view, which is `Project`.
        serializer_class (serializers.ProjectCreationSerializer): The serializer used to validate and
            serialize the project data.
    """
    model = models.Project
    serializer_class = serializers.ProjectCreationSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        transformed_data = camel_case_to_snake_case(request.data)
        serializer = self.get_serializer(
            data=transformed_data, context={'request': request}
        )
        organization_id: UUID = transformed_data.get('organization')

        if not organization_id:
            return Response({'organization': ['This field is required']},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            membership = OrganizationMember.objects.get(
                organization_id=organization_id, user=self.request.user)
        except OrganizationMember.DoesNotExist:
            # Dont allow a person who is not a member of the organization to create a project.
            return Response({
                'non_field_errors': ['You must be a member of the organization to create a project']},
                status=status.HTTP_400_BAD_REQUEST)

        if membership.role != 'Admin':
            return Response({
                'non_field_errors': ['You dont have the necessary permissions to \
                 create a project for this organization']},
                status=status.HTTP_400_BAD_REQUEST)

        if (serializer.is_valid()):
            project = serializer.save()
            project_retrieval_serializer = serializers.ProjectRetrievalSerializer(
                project)
            return Response(project_retrieval_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProjectsListView(generics.ListAPIView):
    """
    Returns all the projects that the user is a member of.
    """
    serializer_class = serializers.ProjectRetrievalSerializer

    def get_queryset(self):
        memberships = self.request.user.projects.all()
        projects = [membership.project for membership in memberships]
        return projects
