from django.db import models


class Video(models.Model):
    """Model representing a video with category, thumbnail and HLS streaming support."""

    CATEGORY_CHOICES = [
        ("Drama", "Drama"),
        ("Romance", "Romance"),
        ("Action", "Action"),
        ("Comedy", "Comedy"),
        ("Documentary", "Documentary"),
    ]

    title = models.CharField(
        max_length=255
    )

    description = models.TextField()

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
    )

    thumbnail = models.ImageField(
        upload_to="thumbnails/",
    )

    original_video = models.FileField(
        upload_to="videos/original/",
    )

    hls_ready = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        """Return the string representation (title) of the video."""
        return self.title
