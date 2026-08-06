import os
import subprocess
from django.conf import settings
from .models import Video


def convert_video_to_hls(video_id):

    video = Video.objects.get(
        id=video_id
    )

    input_path = video.original_video.path

    output_base = os.path.join(
        settings.MEDIA_ROOT,
        "videos",
        str(video.id)
    )

    resolutions = {
        "480p": "854:480",
        "720p": "1280:720",
        "1080p": "1920:1080",
    }

    for resolution, scale in resolutions.items():

        output_path = os.path.join(
            output_base,
            resolution
        )

        os.makedirs(
            output_path,
            exist_ok=True
        )

        playlist = os.path.join(
            output_path,
            "index.m3u8"
        )

        command = [
            "ffmpeg",
            "-i",
            input_path,

            "-vf",
            f"scale={scale}",

            "-codec:v",
            "h264",

            "-codec:a",
            "aac",

            "-start_number",
            "0",

            "-hls_time",
            "10",

            "-hls_list_size",
            "0",

            "-f",
            "hls",

            playlist,
        ]

        subprocess.run(
            command,
            check=True
        )
    video.hls_ready = True
    video.save()
