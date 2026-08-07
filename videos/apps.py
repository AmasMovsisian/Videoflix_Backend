from django.apps import AppConfig


class VideosConfig(AppConfig):
    """App configuration for the videos app, connects signals on ready."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "videos"

    def ready(self):
        """Import signals when the app is ready."""
        import videos.signals