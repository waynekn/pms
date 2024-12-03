from django.contrib import admin
from .models import (Industry, Template, TemplatePhase, Project)

# Register your models here.

admin.site.register(Industry)
admin.site.register(Template)
admin.site.register(TemplatePhase)
admin.site.register(Project)
