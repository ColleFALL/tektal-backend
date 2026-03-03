
# # from django.contrib import admin
# # from paths.models import Path, Step, SavedPath

# # @admin.register(Path)
# # class PathAdmin(admin.ModelAdmin):
# #     list_display = (
# #         'id',
# #         'title',
# #         'author',
# #         'status',
# #         'is_official',
# #         'share_token',
# #         'created_at',
# #     )
# #     list_filter = ('status', 'is_official', 'created_at')
# #     search_fields = ('title', 'start_label', 'end_label', 'author__email')
# #     readonly_fields = (
# #         'author',
# #         'title',
# #         'start_label',
# #         'end_label',
# #         'start_lat',
# #         'start_lng',
# #         'end_lat',
# #         'end_lng',
# #         'video_url',
# #         'duration',
# #         'status',
# #         'is_official',
# #         'share_token',
# #         'created_at',
# #     )

# #     def has_add_permission(self, request):
# #         return False

# #     def has_delete_permission(self, request, obj=None):
# #         return False

# # @admin.register(Step)
# # class StepAdmin(admin.ModelAdmin):
# #     list_display = ('id', 'path', 'step_number', 'text', 'created_at')
# #     list_filter = ('path', 'created_at')
# #     search_fields = ('path__title', 'text')
# #     ordering = ('path', 'step_number')
# #     readonly_fields = ('created_at',)

# # @admin.register(SavedPath)
# # class SavedPathAdmin(admin.ModelAdmin):
# #     list_display = ('id', 'user', 'path', 'created_at')
# #     list_filter = ('user', 'created_at')
# #     search_fields = ('user__email', 'path__title')
# #     ordering = ('-created_at',)
# #     readonly_fields = ('created_at',)
# from django.contrib import admin
# from paths.models import Path, Step, SavedPath

# @admin.register(Path)
# class PathAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'title',
#         'user',
#         'status',
#         'is_official',
#         'share_token',
#         'created_at',
#     )
#     list_filter = ('status', 'is_official', 'created_at')
#     search_fields = ('title', 'start_label', 'end_label', 'user__email')
#     readonly_fields = (
#         'user',
#         'title',
#         'start_label',
#         'end_label',
#         'start_lat',
#         'start_lng',
#         'end_lat',
#         'end_lng',
#         'video_url',
#         'duration',
#         'status',
#         'is_official',
#         'share_token',
#         'created_at',
#     )

#     def has_add_permission(self, request):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

# @admin.register(Step)
# class StepAdmin(admin.ModelAdmin):
#     list_display = ('id', 'path', 'step_number', 'text', 'created_at')
#     list_filter = ('path', 'created_at')
#     search_fields = ('path__title', 'text')
#     ordering = ('path', 'step_number')
#     readonly_fields = ('created_at',)

# @admin.register(SavedPath)
# class SavedPathAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'path', 'created_at')
#     list_filter = ('user', 'created_at')
#     search_fields = ('user__email', 'path__title')
#     ordering = ('-created_at',)
#     readonly_fields = ('created_at',)
from django.contrib import admin
from .models import Path, Step, SavedPath, GPSPoint, Establishment

# 🔹 Admin pour l'établissement
@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'lat', 'lng', 'created_by', 'created_at']
    search_fields = ['name', 'created_by__username']
    readonly_fields = ['created_at']


# 🔹 Admin pour les chemins (Paths)
@admin.register(Path)
class PathAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'establishment', 'user', 'is_official', 'status', 'created_at']
    search_fields = ['title', 'establishment__name', 'user__username']
    list_filter = ['status', 'is_official']
    readonly_fields = ['id', 'created_at']

    # Si tu veux afficher un label pour départ / destination
    def start_label(self, obj):
        return f"{obj.start_lat}, {obj.start_lng}" if obj.start_lat and obj.start_lng else "Non défini"

    def end_label(self, obj):
        return f"{obj.end_lat}, {obj.end_lng}" if obj.end_lat and obj.end_lng else "Non défini"


# 🔹 Admin pour les étapes
@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ['id', 'path', 'step_number', 'start_time', 'end_time', 'text', 'created_at']
    list_filter = ['path']
    readonly_fields = ['id', 'created_at']


# 🔹 Admin pour les chemins sauvegardés
@admin.register(SavedPath)
class SavedPathAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'path', 'created_at']
    readonly_fields = ['id', 'created_at']


# 🔹 Admin pour les points GPS
@admin.register(GPSPoint)
class GPSPointAdmin(admin.ModelAdmin):
    list_display = ['id', 'path', 'order', 'latitude', 'longitude', 'timestamp']
    list_filter = ['path']
    readonly_fields = ['id']