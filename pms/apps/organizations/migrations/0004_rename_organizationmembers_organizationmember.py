# Generated by Django 5.1.2 on 2024-11-28 23:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_organization_organization_name_slug'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrganizationMembers',
            new_name='OrganizationMember',
        ),
    ]
