from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard_view, name='admin_dashboard'),
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('paths/', views.paths_view, name='paths'),
    path('paths/<int:path_id>/', views.path_detail, name='path_detail'),
    path('paths/create/', views.create_path, name='create_path'),
    path('paths/delete/<int:path_id>/', views.delete_path, name='delete_path'),
    path('paths/certify/<int:path_id>/', views.certify_path, name='certify_path'),
    path('users/', views.users_view, name='users'),
    path('users/toggle-admin/<int:user_id>/', views.toggle_admin, name='toggle_admin'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]