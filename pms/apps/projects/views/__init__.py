from .industry import IndustryListView
from .task import ProjectTasksView
from .template import TemplateCreateView, TemplateSearchView
from .project import ProjectCreateView, UserProjectsListView
from .members import (
    ProjectMembersListView,
    NonProjectMemberListView,
    ProjectMemberAdditionView
)
from .phase import (
    ProjectPhaseDetailView,
    ProjectPhaseRetrieveView,
    ProjectPhaseCreateView
)
from .stats import ProjectStatsView

__all__ = [
    'IndustryListView',
    'TemplateCreateView',
    'TemplateSearchView',
    'ProjectCreateView',
    'UserProjectsListView',
    'ProjectMembersListView',
    'NonProjectMemberListView',
    'ProjectMemberAdditionView',
    'ProjectPhaseDetailView',
    'ProjectPhaseRetrieveView',
    'ProjectPhaseCreateView',
    'ProjectTasksView',
    'ProjectStatsView'
]
