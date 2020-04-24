from rest_framework import views, response
from  .models import Song
from .serializer import SongSerializer


# Create your views here.

class ListSongsView (views.APIView):
    """
        Get list of all objects storage at the database
    """
    def get(self, request):
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return response.Response({'songs': serializer.data})


class GetSongById (views.APIView):
    """
        Get a song by ID
    """

    def get(self, request, song_id, format=None):
        song = Song.objects.get(id=song_id)
        serializer = SongSerializer(song)
        return response.Response({'song': serializer.data})




