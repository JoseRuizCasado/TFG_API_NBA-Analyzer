from rest_framework import generics
from  .models import Song
from .serializer import SongSerializer


# Create your views here.
class ListSongsView (generics.ListAPIView):
    """
        Provides a GET method handler
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer