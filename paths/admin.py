from django.contrib import admin
from paths.models import Path, Step, SavedPath

# -------------------------------
# Admin pour Path (inchangé pour les restrictions)
# -------------------------------
@admin.register(Path)
class PathAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'user',
        'status',
        'is_official',
        'created_at',
    )
    list_filter = ('status', 'is_official', 'created_at')
    search_fields = ('title', 'start_label', 'end_label', 'user__email')
    readonly_fields = (
        'user',
        'title',
        'start_label',
        'end_label',
        'start_lat',
        'start_lng',
        'end_lat',
        'end_lng',
        'video_url',
        'duration',
        'status',
        'is_official',
        'created_at',
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# -------------------------------
# Admin pour Step
# -------------------------------
@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('id', 'path', 'step_number', 'text', 'created_at')
    list_filter = ('path', 'created_at')
    search_fields = ('path__title', 'text')
    ordering = ('path', 'step_number')
    readonly_fields = ('created_at',)

# -------------------------------
# Admin pour SavedPath
# -------------------------------
@admin.register(SavedPath)
class SavedPathAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'path', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__email', 'path__title')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
