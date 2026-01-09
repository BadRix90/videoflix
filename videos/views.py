"""Views for video streaming endpoints."""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Video
from .serializers import VideoSerializer
from .utils import serve_manifest, serve_segment


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def video_list_view(request):
    """Return list of all available videos."""
    videos = Video.objects.all()
    serializer = VideoSerializer(videos, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def video_manifest_view(request, movie_id, resolution):
    """Return HLS manifest for video at specified resolution."""
    return serve_manifest(movie_id, resolution)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def video_segment_view(request, movie_id, resolution, segment):
    """Return HLS segment for video playback."""
    return serve_segment(movie_id, resolution, segment)
