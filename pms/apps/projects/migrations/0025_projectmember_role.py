# Generated by Django 5.1.2 on 2025-01-14 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0024_alter_projectphase_phase_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectmember',
            name='role',
            field=models.CharField(choices=[('Manager', 'Manager'), ('Member', 'Member')], default='Member', max_length=50),
        ),
    ]
