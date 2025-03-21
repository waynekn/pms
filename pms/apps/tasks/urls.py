from django.urls import path

from . import views

urlpatterns = [
    path('task/create/', views.TaskCreateView.as_view(), name='create_task'),
    path('task/detail/<str:task_id>/',
         views.TaskDetailView.as_view(), name='task_detail'),
    path('task/<str:task_id>/non-assignees/',
         views.NonTaskAssigneesListView.as_view(), name='non_assignees'),
    path('task/<str:task_id>/assign/',
         views.TaskAssignmentView.as_view(), name='assign_task'),
    path('task/<str:task_id>/status/update/',
         views.TaskStatusUpdateView.as_view(), name='update_task_status'),
    path('assignment/<str:task_id>/delete/',
         views.TaskAssignmentDeleteView.as_view(), name='delete_task_assignment'),
]
