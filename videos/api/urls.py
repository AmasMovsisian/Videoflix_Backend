from django.urls import path

from .views import (
    VideoListView,
    VideoHLSPlaylistView,
    VideoHLSSegmentView,
)


urlpatterns = [

    path(
        "video/",
        VideoListView.as_view(),
        name="video-list",
    ),

    path(
        "video/<int:movie_id>/<str:resolution>/index.m3u8",
        VideoHLSPlaylistView.as_view(),
        name="video-hls-playlist",
    ),

    path(
        "video/<int:movie_id>/<str:resolution>/<str:segment>/",
        VideoHLSSegmentView.as_view(),
        name="video-hls-segment",
    ),

]
