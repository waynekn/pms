# Generated by Django 5.1.2 on 2024-12-23 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_projectphase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='template_name',
            field=models.CharField(max_length=50, verbose_name='Template name'),
        ),
    ]
