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
    path('<str:organization_id>/admins/',
         views.OrganizationAdminsListView.as_view(), name='organization_admins'),
    path('<str:organization_id>/non-admins/',
         views.NonOrganizationAdminsListView.as_view(), name='non_org_admins'),
    path('<str:organization_id>/admins/create/',
         views.OrganizationAdminCreateView.as_view(), name='create_admins'),
    path('<str:organization_id>/admin/revoke/',
         views.OrganizationAdminRoleRevokeView.as_view(), name='remove_admin'),
    path('<str:organization_id>/exit/',
         views.OrgnizationMemberDeleteView.as_view(), name='exit_org'),
    path('auth/',
         views.OrganizationAuthView.as_view(), name='organization_auth'),
]
