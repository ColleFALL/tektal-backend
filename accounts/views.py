from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .models import PasswordResetToken
from .serializers import RegisterSerializer, UserSerializer
from django.shortcuts import render
from django.http import JsonResponse
import requests

User = get_user_model()

def ok(message="", data=None, code=200):
    return Response({"success": True, "message": message, "data": data}, status=code)

def fail(message="", data=None, code=400):
    return Response({"success": False, "message": message, "data": data}, status=code)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return fail("Validation error", serializer.errors, 400)

        email = serializer.validated_data["email"].lower().strip()
        if User.objects.filter(email=email).exists():
            return fail("Email déjà utilisé", None, 409)

        user = serializer.save(email=email)
        return ok("Compte créé", UserSerializer(user).data, 201)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = (request.data.get("email") or "").lower().strip()
        password = request.data.get("password") or ""
        remember = bool(request.data.get("remember", False))

        if not email or not password:
            return fail("Email et mot de passe requis", None, 400)

        user = User.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            return fail("Identifiants invalides", None, 401)

        if not user.is_active:
            return fail("Compte désactivé", None, 403)

        refresh = RefreshToken.for_user(user)
        data = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data,
            "remember": remember,
        }
        return ok("Connecté", data, 200)


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return ok("Profil", UserSerializer(request.user).data, 200)


class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = (request.data.get("email") or "").lower().strip()
        if not email:
            return ok("Si cet email existe, vous recevrez un message.", None, 200)

        user = User.objects.filter(email=email).first()
        if user:
            prt = PasswordResetToken.create_for(user, hours=1)
            print(f"[FORGOT PASSWORD] email={email} token={prt.token} expires={prt.expires_at}")

        return ok("Si cet email existe, vous recevrez un message.", None, 200)


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get("token")
        new_password = request.data.get("new_password") or ""

        if not token or not new_password:
            return fail("Token et nouveau mot de passe requis", None, 400)

        prt = PasswordResetToken.objects.filter(token=token).first()
        if not prt or not prt.is_valid():
            return fail("Token invalide ou expiré", None, 400)

        user = prt.user
        user.set_password(new_password)
        user.save()
        prt.delete()

        return ok("Mot de passe mis à jour", None, 200)
# ============================================
#  NOUVELLE VUE : Page d'activation HTML
# ============================================
def activate_account_page(request, uid, token):
    """
    Page HTML pour activer le compte via un formulaire.
    GET : Affiche la page avec le bouton
    POST : Active le compte via l'API Djoser
    """
    if request.method == 'GET':
        # Afficher la page avec le formulaire
        context = {
            'uid': uid,
            'token': token,
        }
        return render(request, 'accounts/activate.html', context)
    
    elif request.method == 'POST':
        # Traiter l'activation en appelant l'API Djoser
        api_url = f"{request.scheme}://{request.get_host()}/api/auth/users/activation/"
        
        payload = {
            'uid': uid,
            'token': token,
        }
        try:
            response = requests.post(api_url, json=payload)
            
            if response.status_code == 204:
                return JsonResponse({
                    'success': True,
                    'message': ' Votre compte a été activé avec succès !'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': ' Lien d\'activation invalide ou expiré.'
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f' Erreur : {str(e)}'
            }, status=500)