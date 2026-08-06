from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core.cache import cache

from django.conf import settings
from django.http import FileResponse, Http404

import os

from videos.models import Video
from .serializers import VideoSerializer


class VideoListView(generics.ListAPIView):

    serializer_class = VideoSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        cached_videos = cache.get(
            "video_list"
        )

        if cached_videos:
            return cached_videos

        videos = Video.objects.all().order_by(
            "-created_at"
        )

        cache.set(
            "video_list",
            videos,
            timeout=300
        )

        return videos

    serializer_class = VideoSerializer
    queryset = Video.objects.all().order_by("-created_at")
    permission_classes = [
        IsAuthenticated
    ]


class VideoHLSPlaylistView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        movie_id,
        resolution
    ):

        try:
            Video.objects.get(
                id=movie_id
            )

        except Video.DoesNotExist:
            raise Http404(
                "Video nicht gefunden"
            )

        playlist_path = os.path.join(
            settings.MEDIA_ROOT,
            "videos",
            str(movie_id),
            resolution,
            "index.m3u8"
        )

        if not os.path.exists(
            playlist_path
        ):
            raise Http404(
                "HLS Playlist nicht gefunden"
            )

        return FileResponse(
            open(
                playlist_path,
                "rb"
            ),
            content_type="application/vnd.apple.mpegurl"
        )


class VideoHLSSegmentView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        movie_id,
        resolution,
        segment
    ):

        try:
            Video.objects.get(
                id=movie_id
            )

        except Video.DoesNotExist:
            raise Http404(
                "Video nicht gefunden"
            )

        segment_path = os.path.join(
            settings.MEDIA_ROOT,
            "videos",
            str(movie_id),
            resolution,
            segment
        )

        if not os.path.exists(
            segment_path
        ):
            raise Http404(
                "Segment nicht gefunden"
            )

        return FileResponse(
            open(
                segment_path,
                "rb"
            ),
            content_type="video/MP2T"
        )
