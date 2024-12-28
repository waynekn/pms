# Generated by Django 5.1.2 on 2024-12-28 22:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_alter_projectphase_template_phase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='template',
            field=models.ForeignKey(help_text='The template from which this project is based.', null=True, on_delete=django.db.models.deletion.RESTRICT, to='projects.template', verbose_name='Project base template'),
        ),
    ]
