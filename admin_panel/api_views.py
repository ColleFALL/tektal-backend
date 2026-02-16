from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from .models import Path, Step

# -----------------------------
# LISTE DES PARCOURS
# -----------------------------
@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_paths(request):
    paths = Path.objects.all()
    result = []
    for path in paths:
        result.append({
            'id': path.id,
            'title': path.title,
            'type_parcours': path.type_parcours,
            'video_url': path.video_url,
            'author': path.author.username,
            'status': path.status,
            'created_at': path.created_at,
            'steps': [
                {'id': s.id, 'instruction': s.instruction, 'order': s.order, 'timestamp': s.timestamp}
                for s in path.steps.all()
            ]
        })
    return Response(result)

# -----------------------------
# DETAILS D’UN PARCOURS
# -----------------------------
@api_view(['GET'])
@permission_classes([IsAdminUser])
def path_detail(request, path_id):
    try:
        path = Path.objects.get(id=path_id)
    except Path.DoesNotExist:
        return Response({'detail': 'No Path matches the given query.'}, status=status.HTTP_404_NOT_FOUND)

    data = {
        'id': path.id,
        'title': path.title,
        'type_parcours': path.type_parcours,
        'video_url': path.video_url,
        'author': path.author.username,
        'status': path.status,
        'created_at': path.created_at,
        'steps': [
            {'id': s.id, 'instruction': s.instruction, 'order': s.order, 'timestamp': s.timestamp}
            for s in path.steps.all()
        ]
    }
    return Response(data)

# -----------------------------
# APPROUVER UN PARCOURS
# -----------------------------
@api_view(['POST'])
@permission_classes([IsAdminUser])
def approve_path(request, path_id):
    try:
        path = Path.objects.get(id=path_id)
    except Path.DoesNotExist:
        return Response({'detail': 'No Path matches the given query.'}, status=status.HTTP_404_NOT_FOUND)

    path.status = 'APPROVED'
    path.save()
    return Response({'status': 'approved'})

# -----------------------------
# REFUSER UN PARCOURS
# -----------------------------
@api_view(['POST'])
@permission_classes([IsAdminUser])
def reject_path(request, path_id):
    try:
        path = Path.objects.get(id=path_id)
    except Path.DoesNotExist:
        return Response({'detail': 'No Path matches the given query.'}, status=status.HTTP_404_NOT_FOUND)

    path.status = 'REJECTED'
    path.save()
    return Response({'status': 'rejected'})

# -----------------------------
# UTILISATEURS CONNECTÉS
# -----------------------------
@api_view(['GET'])
@permission_classes([IsAdminUser])
def connected_users(request):
    # Récupère toutes les sessions non expirées
    sessions = Session.objects.filter(expire_date__gte=timezone.now())

    users = []
    for session in sessions:
        data = session.get_decoded()
        user_id = data.get('_auth_user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                users.append({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'last_login': user.last_login
                })
            except User.DoesNotExist:
                continue

    return Response(users)
