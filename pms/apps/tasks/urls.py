from django.urls import path

from . import views

urlpatterns = [
    path('task/create/', views.TaskCreateView.as_view(), name='create_task'),
    path('task/detail/<str:task_id>/',
         views.TaskDetailView.as_view(), name='task_detail'),
]
