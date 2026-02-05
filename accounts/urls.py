from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    MeView,
    ForgotPasswordView,
    ResetPasswordView
)

urlpatterns = [
    # Création de compte
    path("register/", RegisterView.as_view(), name="register"),
    
    # Connexion / JWT
    path("login/", LoginView.as_view(), name="login"),
    
    # Profil de l'utilisateur connecté
    path("me/", MeView.as_view(), name="me"),
    
    # Mot de passe oublié
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    
    # Réinitialisation du mot de passe
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
]
