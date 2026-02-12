from django.contrib import admin
from .models import Path, Step

@admin.register(Path)
class PathAdmin(admin.ModelAdmin):
    # On affiche les infos importantes dans la liste
    list_display = ('title', 'type_parcours', 'is_official', 'created_at')
    list_filter = ('type_parcours', 'is_official')
    search_fields = ('title',)

@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('path', 'order', 'instruction')