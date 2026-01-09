"""Utility functions for user authentication."""
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User


def generate_token_data(user):
    """Generate uid and token for user verification."""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    return uid, token


def build_activation_html(link):
    """Build HTML content for activation email."""
    return f'''<html><body>
    <h2>Welcome to Videoflix!</h2>
    <p>Click the button below to activate your account:</p>
    <p><a href="{link}" style="background:#e50914;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">Activate Account</a></p>
    <p>Or copy this link: {link}</p>
    </body></html>'''


def send_activation_email(user, uid, token):
    """Send account activation email to user."""
    link = f"{settings.FRONTEND_URL}/pages/auth/activate.html?uid={uid}&token={token}"
    send_mail(
        subject='Activate your Videoflix account',
        message=f'Activate your account: {link}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=build_activation_html(link),
        fail_silently=False,
    )


def build_reset_html(link):
    """Build HTML content for password reset email."""
    return f'''<html><body>
    <h2>Reset your Videoflix password</h2>
    <p>Click the button below to reset your password:</p>
    <p><a href="{link}" style="background:#e50914;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">Reset Password</a></p>
    <p>Or copy this link: {link}</p>
    </body></html>'''


def send_password_reset_email(user, uid, token):
    """Send password reset email to user."""
    link = f"{settings.FRONTEND_URL}/pages/auth/confirm_password.html?uid={uid}&token={token}"
    send_mail(
        subject='Reset your Videoflix password',
        message=f'Reset your password: {link}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=build_reset_html(link),
        fail_silently=False,
    )


def set_auth_cookies(response, refresh):
    """Set HTTP-only authentication cookies on response."""
    response.set_cookie(
        'access_token', str(refresh.access_token),
        httponly=True, secure=False, samesite='Lax'
    )
    response.set_cookie(
        'refresh_token', str(refresh),
        httponly=True, secure=False, samesite='Lax'
    )
    return response


def delete_auth_cookies(response):
    """Remove authentication cookies from response."""
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response


def get_user_from_uidb64(uidb64):
    """Decode uidb64 and return user or None."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        return User.objects.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist):
        return None


def verify_token(user, token):
    """Verify if token is valid for user."""
    return default_token_generator.check_token(user, token)


def blacklist_refresh_token(refresh_token):
    """Add refresh token to blacklist."""
    from rest_framework_simplejwt.tokens import RefreshToken
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return True
    except Exception:
        return False