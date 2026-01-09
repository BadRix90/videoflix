"""URL configuration for video streaming."""
from django.urls import path
from .views import video_list_view, video_manifest_view, video_segment_view

urlpatterns = [
    path('video/', video_list_view, name='video_list'),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', video_manifest_view, name='video_manifest'),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>/', video_segment_view, name='video_segment'),
]
