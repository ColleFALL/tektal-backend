from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Authentification
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('register/', views.admin_register, name='admin_register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # Mot de passe oublié
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='admin_panel/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='admin_panel/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='admin_panel/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='admin_panel/password_reset_complete.html'), name='password_reset_complete'),

    # Pages principales (Assure-toi que 'paths' est bien ici)
    path('', views.dashboard_view, name='admin_dashboard'),
    path('paths/', views.paths_view, name='paths'), # <--- L'erreur venait d'ici
    path('users/', views.users_view, name='users'),
    
    # Actions
    path('certify/<int:path_id>/', views.certify_path, name='certify_path'),
    path('delete/<int:path_id>/', views.delete_path, name='delete_path'),
    path('toggle-admin/<int:user_id>/', views.toggle_admin, name='toggle_admin'),
]