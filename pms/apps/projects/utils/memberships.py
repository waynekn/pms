from typing import Optional

from .. import models
from apps.users.models import User


def get_project_membership(project: models.Project, user: User) -> Optional[models.ProjectMember]:
    """
    Retrieves a project member.

    This function retrieves a membership for a given project and user
    without considering the role. It returns None if no such membership 
    exists.
    """
    try:
        membership = models.ProjectMember.objects.get(
            project=project, member=user)
        return membership
    except models.ProjectMember.DoesNotExist:
        return None
