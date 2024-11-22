from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Organization


class OrganizationCreateForm(forms.ModelForm):
    """
    Display Organization model form.
    """
    password_confirm = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password (again)'}),
    )

    class Meta:
        model = Organization
        fields = ['organization_name', 'organization_password']
        widgets = {
            'organization_name': forms.TextInput(attrs={'placeholder': 'Enter organization name'}),
            'organization_password': forms.PasswordInput(attrs={'placeholder': 'Enter a secure password'}),
        }
        labels = {
            'organization_password': 'Password',
        }

    def clean_organization_name(self):
        organization_name = self.cleaned_data.get('organization_name')

        if Organization.objects.filter(organization_name=organization_name).exists():
            raise ValidationError(
                "An organization with this name already exists.")

        return organization_name

    def clean_organization_password(self):
        password = self.cleaned_data.get("organization_password")
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('organization_password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")

        return cleaned_data
