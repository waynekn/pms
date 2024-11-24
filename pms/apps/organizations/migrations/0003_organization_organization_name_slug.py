# Generated by Django 5.1.2 on 2024-11-21 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_organizationmembers'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='organization_name_slug',
            field=models.SlugField(max_length=100, null=True, verbose_name='Organization Slug'),
        ),
    ]