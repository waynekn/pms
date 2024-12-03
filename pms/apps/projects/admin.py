from django.contrib import admin
from .models import (Industry, Template, TemplatePhase,
                     CustomPhase, Project, ProjectMember)

# Register your models here.

admin.site.register(Industry)
admin.site.register(Template)
admin.site.register(TemplatePhase)
admin.site.register(CustomPhase)
admin.site.register(Project)
admin.site.register(ProjectMember)
