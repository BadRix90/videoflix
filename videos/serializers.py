"""Serializers for video models."""
from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    """Serializer for video list endpoint."""

    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'created_at', 'title', 'description', 'thumbnail_url', 'category']

    def get_thumbnail_url(self, obj):
        """Return absolute URL for thumbnail."""
        request = self.context.get('request')
        if obj.thumbnail and request:
            return request.build_absolute_uri(obj.thumbnail.url)
        return None
