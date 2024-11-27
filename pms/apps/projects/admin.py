from django.contrib import admin
from .models import (Industry, Template, TemplatePhase)

# Register your models here.

admin.site.register(Industry)

admin.site.register(Template)

admin.site.register(TemplatePhase)
