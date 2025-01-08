from django.urls import path, reverse
from . import views

urlpatterns = [
    path('industry/list/', views.IndustryListView.as_view(), name='industry_list'),
    path('template/create/', views.TemplateCreateView.as_view(),
         name='create_template'),
    path('template/search/', views.TemplateSearchView.as_view(),
         name='template_search'),
    path('project/create/',
         views.ProjectCreateView.as_view(), name='create_project'),
    path('project/stats/',
         views.ProjectStatsView.as_view(), name='project_stats'),
    path('user/projects/',
         views.UserProjectsListView.as_view(), name='user_project_list'),
    path('project/<str:project_id>/members/',
         views.ProjectMembersListView.as_view(), name='project_members_list'),
    path('project/<str:project_id>/non-members/',
         views.NonProjectMemberListView.as_view(), name='non_project_members_list'),
    path('project/<str:project_id>/members/add/',
         views.ProjectMemberAdditionView.as_view(), name='project_members_addition'),
    path('project/<str:project_id>/tasks/',
         views.ProjectTasksView.as_view(), name='project_tasks_retrieval'),
    path('project/<str:project_id>/workflow/',
         views.ProjectPhaseRetrieveView.as_view(), name='project_phases'),
]
