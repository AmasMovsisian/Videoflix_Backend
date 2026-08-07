from django.db.models.signals import post_save
from django.dispatch import receiver
import django_rq
from .models import Video
from .tasks import convert_video_to_hls
from django.core.cache import cache


@receiver(post_save, sender=Video)
def video_post_save(
    sender,
    instance,
    created,
    **kwargs
):
    """Enqueue HLS conversion task for newly created videos and clear cache."""
    if created:
        queue = django_rq.get_queue(
            "default"
        )
        queue.enqueue(
            convert_video_to_hls,
            instance.id,
        )
        cache.delete(
            "video_list"
        )
