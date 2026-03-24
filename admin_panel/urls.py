
from django.urls import path
from . import api_views

urlpatterns = [
    # PATHS
    path('api/paths/', api_views.PathListView.as_view(), name='paths-list'),
    path('api/paths/public/', api_views.PublicPathListAPI.as_view(), name='paths-public'),
    path('api/paths/approve/<int:pk>/', api_views.PathApproveView.as_view(), name='paths-approve'),
    path('api/paths/reject/<int:pk>/', api_views.PathRejectView.as_view(), name='paths-reject'),
    path('api/paths/<int:pk>/', api_views.PathDetailView.as_view(), name='paths-detail'),
    path('api/paths/<int:pk>/delete/', api_views.PathDeleteView.as_view(), name='path-delete'),
    path('api/paths/<int:pk>/hide/', api_views.PathHideView.as_view(), name='path-hide'),

    # USERS
    path('api/users/connected/', api_views.ConnectedUsersView.as_view(), name='users-connected'),
    path('api/users/<int:pk>/delete/', api_views.UserDeleteView.as_view(), name='user-delete'),
    path('api/users/<int:pk>/toggle-admin/', api_views.UserToggleAdminView.as_view(), name='user-toggle-admin'),
    path('api/users/<int:pk>/toggle-etablissement/', api_views.UserToggleEtablissementView.as_view(), name='user-toggle-etablissement'),
    # path('api/users/<int:pk>/toggle-role/', api_views.UserToggleRoleView.as_view(), name='user-toggle-role'),

    # ADMIN / SETUP
    path('api/admin/login/', api_views.AdminLoginView.as_view(), name='admin-login'),
    path('api/setup/', api_views.SetupAdminView.as_view(), name='setup-admin'),

    # ETABLISSEMENTS
    path('api/etablissements/', api_views.EtablissementListView.as_view(), name='etablissements-list'),
    path('api/etablissements/<int:pk>/delete/', api_views.EtablissementDeleteView.as_view(), name='etablissement-delete'),
    path('api/etablissement/profile/', api_views.EtablissementProfileView.as_view(), name='etablissement-profile'),
    path('api/etablissement/paths/', api_views.EtablissementPathListView.as_view(), name='etablissement-paths'),
    path('api/etablissement/paths/approve/<int:pk>/', api_views.EtablissementPathApproveView.as_view(), name='etablissement-path-approve'),
    path('api/etablissement/paths/reject/<int:pk>/', api_views.EtablissementPathRejectView.as_view(), name='etablissement-path-reject'),
    path('api/etablissement/paths/<int:pk>/delete/', api_views.EtablissementPathDeleteView.as_view(), name='etablissement-path-delete'),
    path('api/etablissement/paths/<int:pk>/hide/', api_views.EtablissementPathHideView.as_view(), name='etablissement-path-hide'), 
]