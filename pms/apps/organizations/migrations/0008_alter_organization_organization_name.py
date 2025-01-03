# Generated by Django 5.1.2 on 2024-12-31 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0007_remove_organization_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='organization_name',
            field=models.CharField(error_messages={'unique': 'An organization with this name already exists.'}, max_length=50, unique=True, verbose_name='Organization name'),
        ),
    ]
