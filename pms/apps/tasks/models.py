from django.db import models
from apps.projects.models import ProjectPhase, Project
from apps.users.models import User

from pms.utils import base_62_pk

# Create your models here.


class Task(models.Model):
    """
    Represents a task within a task collection.
    """

    IN_PROGRESS = "IN_PROGRESS"
    ON_HOLD = "ON_HOLD"
    DONE = "DONE"

    TASK_STATUS_CHOICES = [
        (IN_PROGRESS, "In progress"),
        (ON_HOLD, "ON_HOLD"),
        (DONE, "Done"),
    ]
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='tasks', default=None)
    task_id = models.CharField(
        verbose_name="Task ID", primary_key=True, max_length=11, unique=True, editable=False, default=base_62_pk)
    task_name = models.CharField(verbose_name='Task name',
                                 db_comment='Task name unique within a task collection', max_length=30)
    start_date = models.DateField(verbose_name='Start date', auto_now_add=True)
    deadline = models.DateField(verbose_name='Deadline data')
    description = models.TextField(
        max_length=500, default='')
    status = models.CharField(
        max_length=15,
        choices=TASK_STATUS_CHOICES,
        default=IN_PROGRESS,
        help_text="The current status of the task.",
        verbose_name="Task status"
    )

    def __str__(self):
        return f'{self.project.project_name} | {self.task_name}'


class TaskAssignment(models.Model):
    """
    Represents users who have been assigned a task.
    """
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='assignments')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return f'{self.user.username} | {self.task.task_name}'
