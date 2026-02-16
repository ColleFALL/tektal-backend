from django.urls import path
from . import api_views

urlpatterns = [
    # Parcs
    path('api/paths/', api_views.list_paths, name='list_paths'),
    path('api/paths/<int:path_id>/', api_views.path_detail, name='path_detail'),
    path('api/paths/approve/<int:path_id>/', api_views.approve_path, name='approve_path'),
    path('api/paths/reject/<int:path_id>/', api_views.reject_path, name='reject_path'),

    # Utilisateurs connectés
    path('api/connected-users/', api_views.connected_users, name='connected_users'),
]
