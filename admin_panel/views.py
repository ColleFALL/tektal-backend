from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Path 

User = get_user_model()

def is_admin(user):
    return user.is_authenticated and user.is_staff

# --- AUTHENTIFICATION ---
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_panel:admin_dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect('admin_panel:admin_dashboard')
            else:
                messages.error(request, "Accès refusé : Ce compte n'est pas Admin.")
        else:
            messages.error(request, "Identifiants invalides.")
    else:
        form = AuthenticationForm()
    return render(request, 'admin_panel/login.html', {'form': form})

def admin_logout(request):
    logout(request)
    return redirect('admin_panel:admin_login')

# --- GESTION DES CHEMINS ---
@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def paths_view(request):
    paths = Path.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/paths.html', {'paths': paths})

@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def certify_path(request, path_id):
    path = get_object_or_404(Path, id=path_id)
    path.is_official = True
    path.save()
    messages.success(request, f"Le trajet '{path.title}' est maintenant officiel.")
    return redirect('admin_panel:paths')

@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def delete_path(request, path_id):
    path = get_object_or_404(Path, id=path_id)
    path.delete()
    messages.warning(request, "Trajet supprimé.")
    return redirect('admin_panel:paths')

# --- GESTION DES UTILISATEURS ---
@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def users_view(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_panel/users.html', {'users': users})

@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def toggle_admin(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if not target_user.is_superuser:
        target_user.is_staff = not target_user.is_staff
        target_user.save()
        status = "promu Admin" if target_user.is_staff else "rétrogradé Membre"
        messages.success(request, f"{target_user.username} a été {status}.")
    return redirect('admin_panel:users')

# --- DASHBOARD ---
@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def dashboard_view(request):
    context = {
        'total_paths': Path.objects.count(),
        'official_count': Path.objects.filter(is_official=True).count(),
        'user_count': User.objects.count(),
    }
    return render(request, 'admin_panel/dashboard.html', context)