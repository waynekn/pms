from django.urls import path
from . import views

urlpatterns = [
    path('industry/list/', views.IndustryListView.as_view(), name='industry_list'),
    path('template/create/', views.TemplateCreateView.as_view(),
         name='create_template'),
    path('template/search/', views.TemplateSearchView.as_view(),
         name='template_search'),
    path('project/create/',
         views.ProjectCreateView.as_view(), name='create_project'),
]
