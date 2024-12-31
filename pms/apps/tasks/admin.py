from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.TaskCollection)
admin.site.register(models.TaskAssignment)
admin.site.register(models.Task)
