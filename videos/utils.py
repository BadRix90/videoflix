"""Utility functions for video streaming."""
import os
from django.conf import settings
from django.http import FileResponse, Http404


def get_hls_base_path(movie_id, resolution):
    """Return base path for HLS files."""
    return os.path.join(settings.MEDIA_ROOT, 'hls', str(movie_id), resolution)


def get_manifest_path(movie_id, resolution):
    """Return path to HLS manifest file."""
    base = get_hls_base_path(movie_id, resolution)
    return os.path.join(base, 'index.m3u8')


def get_segment_path(movie_id, resolution, segment):
    """Return path to HLS segment file."""
    base = get_hls_base_path(movie_id, resolution)
    return os.path.join(base, segment)


def serve_file(file_path, content_type):
    """Serve file as FileResponse or raise 404."""
    if not os.path.exists(file_path):
        raise Http404("File not found")
    return FileResponse(open(file_path, 'rb'), content_type=content_type)


def serve_manifest(movie_id, resolution):
    """Serve HLS manifest file."""
    path = get_manifest_path(movie_id, resolution)
    return serve_file(path, 'application/vnd.apple.mpegurl')


def serve_segment(movie_id, resolution, segment):
    """Serve HLS segment file."""
    path = get_segment_path(movie_id, resolution, segment)
    return serve_file(path, 'video/MP2T')
