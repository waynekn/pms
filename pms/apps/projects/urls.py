from django.urls import path
from .views import TemplateCreateView, ProjectCreateView, IndustryListView

urlpatterns = [
    path('industry/list/', IndustryListView.as_view(), name='industry_list'),
    path('template/create/', TemplateCreateView.as_view(), name='create_template'),
    path('<slug:organization_name_slug>/project/create/',
         ProjectCreateView.as_view(), name='create_project'),
]
