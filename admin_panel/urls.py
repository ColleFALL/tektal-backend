from django.urls import path
from . import views

app_name = 'admin_panel'

# Vérifie bien l'orthographe exacte : urlpatterns (tout en minuscule)
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('paths/', views.paths, name='paths'),
    path('users/', views.users, name='users'),
]