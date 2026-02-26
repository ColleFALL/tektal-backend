# from django.urls import path
# from paths.views.path_views import PathCreateView, PathListView, PathDetailView
# from paths.views.favorite_views import FavoriteToggleView, FavoriteListView
# from paths.views.share_views import SharePathView
# urlpatterns = [
#     path('paths/', PathListView.as_view(), name='path-list'),
#     path('paths/create/', PathCreateView.as_view(), name='path-create'),
#     path('paths/<int:pk>/', PathDetailView.as_view(), name='path-detail'),  # <- à ajouter
#     path('paths/<int:path_id>/favorite/', FavoriteToggleView.as_view(), name='path-favorite'),
#     path('users/me/favorites/', FavoriteListView.as_view(), name='user-favorites'),
#     # path('share/<int:id>/', SharePathView.as_view(), name='share-path'),
#     path('share/<uuid:share_token>/', SharePathView.as_view(), name='share-path'),  #  UUID

# ]


