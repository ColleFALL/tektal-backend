from django.urls import path
from . import api_views

urlpatterns = [
    path('api/paths/', api_views.PathListView.as_view(), name='paths-list'),
    path('api/paths/public/', api_views.PublicPathListAPI.as_view(), name='paths-public'),
    path('api/paths/approve/<int:pk>/', api_views.PathApproveView.as_view(), name='paths-approve'),
    path('api/paths/reject/<int:pk>/', api_views.PathRejectView.as_view(), name='paths-reject'),
    path('api/paths/<int:pk>/', api_views.PathDetailView.as_view(), name='paths-detail'),
    path('api/users/connected/', api_views.ConnectedUsersView.as_view(), name='users-connected'),
    path('api/admin/login/', api_views.AdminLoginView.as_view(), name='admin-login'),
    path('api/users/<int:pk>/delete/', api_views.UserDeleteView.as_view(), name='user-delete'),
path('api/users/<int:pk>/toggle-admin/', api_views.UserToggleAdminView.as_view(), name='user-toggle-admin'),
]
