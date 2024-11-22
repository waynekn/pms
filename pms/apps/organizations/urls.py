from django.urls import path

from .views import UserOrganizationListView, OrganizationCreateView

urlpatterns = [
    path('', UserOrganizationListView.as_view(), name='user_organizations'),
    path('create/', OrganizationCreateView.as_view(), name='create_organization'),
]
