from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q 
from .models import Path, Step 

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
        messages.error(request, "Identifiants invalides ou accès refusé.")
    return render(request, 'admin_panel/login.html', {'form': AuthenticationForm()})

def admin_logout(request):
    logout(request)
    return redirect('admin_panel:admin_login')

# --- DASHBOARD ---
@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def dashboard_view(request):
    context = {
        'total_paths': Path.objects.count(),
        'official_count': Path.objects.filter(is_official=True).count(),
        'user_count': User.objects.count(),
        'recent_paths': Path.objects.all().order_by('-created_at')[:5],
    }
    return render(request, 'admin_panel/dashboard.html', context)

# --- GESTION DES PARCOURS ---
@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def paths_view(request):
    paths = Path.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/paths.html', {'paths': paths})

@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def create_path(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        type_p = request.POST.get('type_parcours')
        v_url = request.POST.get('video_url')
        if title and v_url:
            Path.objects.create(title=title, type_parcours=type_p, video_url=v_url, author=request.user)
            messages.success(request, "Parcours créé avec succès.")
    return redirect('admin_panel:paths')


@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def path_detail(request, path_id):
    path = get_object_or_404(Path, id=path_id)
    steps = path.steps.all().order_by('order')
    if request.method == 'POST':
        instruction = request.POST.get('instruction')
        timestamp = request.POST.get('timestamp')
        if instruction and timestamp:
            Step.objects.create(
                path=path, 
                instruction=instruction, 
                timestamp=timestamp, 
                order=steps.count() + 1
            )
            messages.success(request, "Étape ajoutée au parcours.")
            return redirect('admin_panel:path_detail', path_id=path.id)
    return render(request, 'admin_panel/path_detail.html', {'path': path, 'steps': steps})

@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def delete_path(request, path_id):
    get_object_or_404(Path, id=path_id).delete()
    messages.info(request, "Parcours supprimé.")
    return redirect('admin_panel:paths')

@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def certify_path(request, path_id):
    p = get_object_or_404(Path, id=path_id)
    p.is_official = not p.is_official
    p.save()
    return redirect('admin_panel:paths')

# --- GESTION UTILISATEURS ---
@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def users_view(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        ).order_by('-last_login')
    else:
        users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_panel/users.html', {'users': users, 'query': query})

@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def toggle_admin(request, user_id):
    u = get_object_or_404(User, id=user_id)
    if not u.is_superuser:
        u.is_staff = not u.is_staff
        u.save()
        messages.success(request, f"Droits de {u.username} modifiés.")
    return redirect('admin_panel:users')

@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def delete_user(request, user_id):
    u = get_object_or_404(User, id=user_id)
    if not u.is_superuser and u != request.user:
        u.delete()
        messages.success(request, "Utilisateur supprimé définitivement.")
    return redirect('admin_panel:users')