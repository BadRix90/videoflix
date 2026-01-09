"""Admin configuration for video models."""
from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Admin interface for Video model."""

    list_display = ['title', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at']
