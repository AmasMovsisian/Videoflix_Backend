from rest_framework import generics
from videos.models import Video
from .serializers import VideoSerializer


class VideoListView(generics.ListAPIView):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()