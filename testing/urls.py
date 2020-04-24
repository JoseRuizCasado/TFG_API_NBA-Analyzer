from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ListSongsView, GetSongById


urlpatterns = [
    path('songs/', ListSongsView.as_view(), name='songs-all'),
    path('song/<int:song_id>', GetSongById.as_view(), name='get-song-by-id')
]

urlpatterns = format_suffix_patterns(urlpatterns)

