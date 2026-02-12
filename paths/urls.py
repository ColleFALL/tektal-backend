from django.urls import path
from paths.views.path_views import PathCreateView, PathListView

urlpatterns = [
    path('paths/', PathListView.as_view(), name='path-list'),
    path('paths/create/', PathCreateView.as_view(), name='path-create'),
]


