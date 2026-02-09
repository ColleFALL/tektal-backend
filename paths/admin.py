from django.contrib import admin
from paths.models import Path


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
