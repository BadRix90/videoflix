"""Background tasks for video processing."""
import subprocess
import os
from django.conf import settings


def convert_to_hls(video_pk):
    """Convert video to HLS format in multiple resolutions."""
    from .models import Video
    video = Video.objects.get(pk=video_pk)
    source_path = video.video_file.path
    output_base = os.path.join(settings.MEDIA_ROOT, 'hls', str(video_pk))
    os.makedirs(output_base, exist_ok=True)
    resolutions = ['480p', '720p', '1080p']
    for resolution in resolutions:
        convert_resolution(source_path, output_base, resolution)


def convert_resolution(source_path, output_base, resolution):
    """Convert video to specific resolution."""
    output_dir = os.path.join(output_base, resolution)
    os.makedirs(output_dir, exist_ok=True)
    scale = get_scale_filter(resolution)
    output_path = os.path.join(output_dir, 'index.m3u8')
    cmd = build_ffmpeg_command(source_path, output_path, scale)
    subprocess.run(cmd, check=True)


def get_scale_filter(resolution):
    """Return FFMPEG scale filter for resolution."""
    scale_map = {
        '480p': 'scale=-2:480',
        '720p': 'scale=-2:720',
        '1080p': 'scale=-2:1080',
    }
    return scale_map.get(resolution, 'scale=-2:480')


def build_ffmpeg_command(source, output, scale):
    """Build FFMPEG command for HLS conversion."""
    return [
        'ffmpeg', '-i', source,
        '-vf', scale,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-start_number', '0',
        '-hls_time', '10',
        '-hls_list_size', '0',
        '-f', 'hls',
        output
    ]
