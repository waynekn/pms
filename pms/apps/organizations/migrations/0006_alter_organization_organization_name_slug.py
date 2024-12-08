# Generated by Django 5.1.2 on 2024-12-04 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0005_alter_organization_organization_name_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='organization_name_slug',
            field=models.SlugField(default=None, max_length=100, unique=True, verbose_name='Organization Slug'),
        ),
    ]