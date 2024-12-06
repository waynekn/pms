from django.urls import path
from .views import TemplateCreateView, ProjectCreateView

urlpatterns = [
    path('template/create/', TemplateCreateView.as_view(), name='create_template'),
    path('<slug:organization_name_slug>/project/create/',
         ProjectCreateView.as_view(), name='create_project'),
]
