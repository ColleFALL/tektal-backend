from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='admin_dashboard'),
    path('certify/<int:path_id>/', views.certify_path, name='certify_path'),
    path('delete/<int:path_id>/', views.delete_path, name='delete_path'),
app_name = 'admin_panel'

# Vérifie bien l'orthographe exacte : urlpatterns (tout en minuscule)
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('paths/', views.paths, name='paths'),
    path('users/', views.users, name='users'),
]