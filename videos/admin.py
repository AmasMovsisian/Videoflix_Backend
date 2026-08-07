from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Admin interface configuration for the Video model."""

    list_display = (
        "id",
        "title",
        "category",
        "hls_ready",
        "created_at",
    )

    list_filter = (
        "category",
        "hls_ready",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
    )

    readonly_fields = (
        "hls_ready",
        "created_at",
    )

    ordering = (
        "-created_at",
    )
