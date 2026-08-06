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
        "480p": {
            "scale": "854:480",
            "bandwidth": "800000",
            "resolution": "854x480",
        },

        "720p": {
            "scale": "1280:720",
            "bandwidth": "1400000",
            "resolution": "1280x720",
        },

        "1080p": {
            "scale": "1920:1080",
            "bandwidth": "3000000",
            "resolution": "1920x1080",
        },
    }

    for resolution, data in resolutions.items():

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
            f"scale={data['scale']}",

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

    # Nach erfolgreicher Erstellung aller Streams
    create_master_playlist(video.id)

    video.hls_ready = True

    video.save()


def create_master_playlist(video_id):

    hls_path = os.path.join(
        settings.MEDIA_ROOT,
        "videos",
        str(video_id)
    )

    master_path = os.path.join(
        hls_path,
        "master.m3u8"
    )

    content = """#EXTM3U
#EXT-X-VERSION:3

#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=854x480
480p/index.m3u8

#EXT-X-STREAM-INF:BANDWIDTH=1400000,RESOLUTION=1280x720
720p/index.m3u8

#EXT-X-STREAM-INF:BANDWIDTH=3000000,RESOLUTION=1920x1080
1080p/index.m3u8
"""

    os.makedirs(
        hls_path,
        exist_ok=True
    )

    with open(
        master_path,
        "w"
    ) as file:

        file.write(content)

    return master_path
