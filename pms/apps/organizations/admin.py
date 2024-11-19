from django.contrib import admin

from .models import Organization, OrganizationMembers

# Register your models here.

admin.site.register(Organization)
admin.site.register(OrganizationMembers)
