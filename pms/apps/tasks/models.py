import uuid
from django.db import models
from apps.projects.models import ProjectPhase

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
    project_phase = models.ForeignKey(ProjectPhase, on_delete=models.CASCADE)
