# Generated by Django 5.1.2 on 2024-12-03 11:01

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_projectmember'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomPhase',
            fields=[
                ('phase_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Phase ID')),
                ('phase_name', models.CharField(help_text='The name of the project phase.', max_length=50, verbose_name='Phase name')),
                ('project', models.ForeignKey(help_text='The project which created this phase', on_delete=django.db.models.deletion.CASCADE, related_name='custom_phases', to='projects.project', verbose_name='Project')),
            ],
        ),
    ]
