from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return JsonResponse({"success": True, "message": "TEKTAL API is running"})

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),

    #  Auth custom (Register, Login, Me, Forgot, Reset)
    path("api/auth/", include("accounts.urls")),

  
]

# Servir les médias en dev
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
