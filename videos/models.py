"""Video models for Videoflix."""
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq


class Video(models.Model):
    """Model representing a video in the platform."""

    CATEGORY_CHOICES = [
        ('drama', 'Drama'),
        ('romance', 'Romance'),
        ('comedy', 'Comedy'),
        ('action', 'Action'),
        ('documentary', 'Documentary'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """Trigger HLS conversion after video upload."""
    if created:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue('videos.tasks.convert_to_hls', instance.pk)


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    """Delete video files when video is deleted."""
    if instance.video_file:
        instance.video_file.delete(save=False)
    if instance.thumbnail:
        instance.thumbnail.delete(save=False)
