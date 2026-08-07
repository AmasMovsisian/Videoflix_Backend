from rest_framework import serializers

from videos.models import Video


class VideoSerializer(serializers.ModelSerializer):
    """Serializer for video objects with absolute thumbnail URL."""

    thumbnail_url = serializers.SerializerMethodField()

    class Meta:

        model = Video

        fields = [
            "id",
            "created_at",
            "title",
            "description",
            "thumbnail_url",
            "category",
        ]

    def get_thumbnail_url(
        self,
        obj,
    ):
        """Return the absolute URL for the thumbnail if available, else None."""
        request = self.context.get(
            "request"
        )

        if obj.thumbnail:

            if request:

                return request.build_absolute_uri(
                    obj.thumbnail.url
                )

            return obj.thumbnail.url

        return None
