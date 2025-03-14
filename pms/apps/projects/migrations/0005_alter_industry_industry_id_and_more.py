# Generated by Django 5.1.2 on 2024-11-26 13:30

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_template_industry_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industry',
            name='industry_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Industry ID'),
        ),
        migrations.AlterField(
            model_name='industry',
            name='industry_name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Industry name'),
        ),
    ]
