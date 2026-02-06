from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Authentification
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    
    # Pages principales
    path('', views.dashboard_view, name='admin_dashboard'),
    path('paths/', views.paths_view, name='paths'),
    path('users/', views.users_view, name='users'),
    
    # Actions (Certifier, Supprimer, Gérer les droits)
    path('certify/<int:path_id>/', views.certify_path, name='certify_path'),
    path('delete/<int:path_id>/', views.delete_path, name='delete_path'),
    path('toggle-admin/<int:user_id>/', views.toggle_admin, name='toggle_admin'), # Correction ici
]