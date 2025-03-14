# Generated by Django 5.1.2 on 2024-12-03 11:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_project'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Project Member')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='projects.project', verbose_name='Project')),
            ],
        ),
    ]
