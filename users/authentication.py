"""Custom JWT authentication using HTTP-only cookies."""
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """Authenticate users via JWT stored in HTTP-only cookies."""

    def authenticate(self, request):
        """Extract and validate JWT from cookies."""
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return None
        validated_token = self.get_validated_token(access_token)
        user = self.get_user(validated_token)
        return (user, validated_token)