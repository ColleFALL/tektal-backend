from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Path

# Fonction de vérification : l'utilisateur est-il un admin ?
# (On vérifie soit le statut is_staff, soit un groupe, selon ce que ton collègue a défini)
def is_admin(user):
    return user.is_authenticated and (user.is_staff or getattr(user, 'role', '') == 'admin')

# --- DASHBOARD (Protégé) ---

@user_passes_test(is_admin, login_url='login') # Redirige si pas admin
def dashboard_view(request):
    paths = Path.objects.all().order_by('-created_at')
    
    context = {
        'paths': paths,
        'total_paths': paths.count(),
        'official_count': paths.filter(is_official=True).count(),
        'pending_count': paths.filter(is_official=False).count(),
    }
    return render(request, 'admin_panel/dashboard.html', context)

# --- ACTIONS DE GESTION ---

@user_passes_test(is_admin)
def certify_path(request, path_id):
    path = get_object_or_404(Path, id=path_id)
    path.is_official = True
    path.save()
    messages.success(request, f"Le trajet '{path.title}' a été certifié avec succès.")
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def delete_path(request, path_id):
    path = get_object_or_404(Path, id=path_id)
    path.delete()
    messages.warning(request, "Le trajet a été supprimé de la plateforme.")
    return redirect('admin_dashboard')