from django.contrib import admin
from .models import Path, Step

@admin.register(Path)
class PathAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'type_parcours', 'created_at')
    search_fields = ('title', 'author__username')
    ordering = ('-created_at',)

@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('path', 'order', 'instruction', 'timestamp')
    ordering = ('path', 'order')
