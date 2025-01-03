import uuid
from django.db import models
from apps.projects.models import ProjectPhase, Project
from apps.users.models import User

# Create your models here.


class TaskCollection(models.Model):
    """
    Container for a collection of tasks within a project phase.

    For example a project is in the testing phase, a task collection would be
    something like "test views" which contains tasks related to testing views.
    """
    collection_id = models.UUIDField(verbose_name='Collection ID', primary_key=True,
                                     unique=True, editable=False, default=uuid.uuid4)
    collection_name = models.CharField(
        verbose_name='Task name', db_comment='Collection name unique in the phase of the project', max_length=100)
    project_phase = models.ForeignKey(
        ProjectPhase, on_delete=models.CASCADE, related_name='task_collections')


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

    collection = models.ForeignKey(
        TaskCollection, on_delete=models.CASCADE, related_name='tasks')
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='tasks', default=None)
    task_id = models.UUIDField(
        verbose_name="Task ID", primary_key=True,  unique=True, editable=False, default=uuid.uuid4)
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


class TaskAssignment(models.Model):
    """
    Represents users who have been assigned a task.
    """
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='assignments')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks')
