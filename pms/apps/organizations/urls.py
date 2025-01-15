from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserOrganizationListView.as_view(), name='user_organizations'),
    path('create/', views.OrganizationCreateView.as_view(),
         name='create_organization'),
    path('search/', views.OrganizationSearchView.as_view(),
         name='organization_search'),
    path('<str:organization_name_slug>/detail/',
         views.OrganizationDetailView.as_view(), name='organization_detail'),
    path('auth/',
         views.OrganizationAuthView.as_view(), name='organization_auth'),
]
