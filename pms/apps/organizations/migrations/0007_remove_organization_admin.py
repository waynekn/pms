# Generated by Django 5.1.2 on 2024-12-28 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0006_alter_organization_organization_name_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='admin',
        ),
    ]
