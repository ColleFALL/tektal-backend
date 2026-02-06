from django.contrib import admin
from .models import Path

@admin.register(Path)
class PathAdmin(admin.ModelAdmin):
    list_display = ('title', 'campus', 'is_official', 'is_active', 'created_at')
    list_filter = ('is_official', 'campus')
    search_fields = ('title',)  