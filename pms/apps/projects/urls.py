from django.urls import path
from .views import TemplateCreateView

urlpatterns = [
    path('template/create/', TemplateCreateView.as_view(), name='create_template'),
]
