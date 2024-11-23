from django.urls import path

from .views import (UserOrganizationListView,
                    OrganizationCreateView, OrganizationSearchView)

urlpatterns = [
    path('', UserOrganizationListView.as_view(), name='user_organizations'),
    path('create/', OrganizationCreateView.as_view(), name='create_organization'),
    path('search/', OrganizationSearchView.as_view(), name='organization_search'),
]
