# Generated by Django 5.1.2 on 2024-12-31 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_taskassignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='description',
            field=models.TextField(default='', max_length=500),
        ),
    ]
