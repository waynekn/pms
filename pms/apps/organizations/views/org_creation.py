from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response

from pms.utils import camel_case_to_snake_case
from apps.organizations.models import Organization
from apps.organizations import serializers


class OrganizationCreateView(generics.CreateAPIView):
    """
    Creates an organization, saves it to the database and adds the
    user who creates the organization to its members.
    """
    model = Organization
    serializer_class = serializers.OrganizationCreationSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        transformed_data = camel_case_to_snake_case(request.data)
        serializer = self.get_serializer(
            data=transformed_data, context={'request': request})

        if (serializer.is_valid()):
            organization = serializer.save()
            retrieval_serializer = serializers.OrganizationRetrievalSerializer(
                organization)
            return Response(retrieval_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
