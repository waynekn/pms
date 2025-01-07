from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Organization, OrganizationMember
from .utils import slugify_organization_name


class OrganizationCreationSerializer(serializers.ModelSerializer):
    """
    Serializer for creating organizations.
    """
    class Meta:
        model = Organization
        fields = ['organization_id', 'organization_name',
                  'organization_name_slug', 'organization_password']

    def validate_organization_name(self, value):
        value = str(value).strip() if value else ""

        if not value:
            serializers.ValidationError("Organization name is required.")

        if Organization.objects.filter(organization_name=value).exists():
            raise serializers.ValidationError(
                "An organization with this name already exists.")
        return value

    def validate_organization_password(self, value):
        value = str(value).strip() if value else ""
        validate_password(value)
        return value

    def validate(self, attrs):
        request = self.context.get('request')
        password1 = attrs.get('organization_password')
        password2 = request.data.get('password2')
        password2 = str(password2).strip() if password2 else ""

        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return super().validate(attrs)

    def save(self, **kwargs):
        user = self.context['request'].user

        validated_data = {
            **self.validated_data,
            'organization_name_slug': slugify_organization_name(self.validated_data['organization_name']),
            'organization_password': make_password(self.validated_data['organization_password'])
        }

        organization = Organization.objects.create(**validated_data)

        OrganizationMember.objects.create(
            organization=organization,
            user=user
        )

        return organization


class OrganizationRetrievalSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving organization(s).
    """
    class Meta:
        model = Organization
        fields = ['organization_id', 'organization_name',
                  'organization_name_slug']
