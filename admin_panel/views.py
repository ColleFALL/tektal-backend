from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail

from .models import Path 
from .forms import SignUpForm
from .tokens import account_activation_token

User = get_user_model()

def is_admin(user):
    return user.is_authenticated and user.is_staff

# --- AUTHENTIFICATION ---

def admin_register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activez votre compte Tektal Admin'
            message = render_to_string('admin_panel/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(subject, message, 'noreply@tektal.com', [user.email])
            return render(request, 'admin_panel/registration_pending.html')
    else:
        form = SignUpForm()
    return render(request, 'admin_panel/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_staff = True
        user.save()
        messages.success(request, 'Compte activé !')
        return redirect('admin_panel:admin_login')
    return render(request, 'admin_panel/activation_invalid.html')

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
            messages.error(request, "Accès refusé.")
    else:
        form = AuthenticationForm()
    return render(request, 'admin_panel/login.html', {'form': form})

def admin_logout(request):
    logout(request)
    return redirect('admin_panel:admin_login')

# --- GESTION ---

@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def dashboard_view(request):
    context = {
        'total_paths': Path.objects.count(),
        'official_count': Path.objects.filter(is_official=True).count(),
        'user_count': User.objects.count(),
    }
    return render(request, 'admin_panel/dashboard.html', context)

@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def paths_view(request):
    paths = Path.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/paths.html', {'paths': paths})

@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def users_view(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_panel/users.html', {'users': users})

@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def certify_path(request, path_id):
    path = get_object_or_404(Path, id=path_id)
    path.is_official = True
    path.save()
    return redirect('admin_panel:paths')

@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def delete_path(request, path_id):
    path = get_object_or_404(Path, id=path_id)
    path.delete()
    return redirect('admin_panel:paths')

@user_passes_test(is_admin, login_url='admin_panel:admin_login')
def toggle_admin(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if not target_user.is_superuser:
        target_user.is_staff = not target_user.is_staff
        target_user.save()
    return redirect('admin_panel:users')