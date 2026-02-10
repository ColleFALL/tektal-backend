from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
# from accounts.views import activate_account_page

def home(request):
    return JsonResponse({"success": True, "message": "TEKTAL API is running"})

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),

    #  Auth via Djoser (register, activation, login, me, reset password)
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    #  Endpoints de l’app paths
    # path("api/", include("paths.urls")),  # <--- on inclut ici
]

# Servir les médias en dev
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
