from django.urls import path
from .views import TemplateCreateView, ProjectCreateView, IndustryListView, TemplateSearchView

urlpatterns = [
    path('industry/list/', IndustryListView.as_view(), name='industry_list'),
    path('template/create/', TemplateCreateView.as_view(), name='create_template'),
    path('template/search/', TemplateSearchView.as_view(), name='template_search'),
    path('project/create/',
         ProjectCreateView.as_view(), name='create_project'),
]
