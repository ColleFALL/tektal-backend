# from django.shortcuts import render

# # Create your views here.

from django.shortcuts import render

def dashboard(request):
    return render(request, 'admin_panel/dashboard.html')

def paths(request):
    return render(request, 'admin_panel/paths.html')

def users(request):
    return render(request, 'admin_panel/users.html')
