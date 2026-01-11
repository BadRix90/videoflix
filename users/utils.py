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


def get_logo_html():
    """Return Videoflix logo HTML."""
    return '''
    <div style="font-size:28px;font-weight:bold;">
        <span style="color:#4D63D5;">&#9658;</span>
        <span style="color:#4D63D5;">VIDEO</span><span style="color:#0D0D0D;">FLIX</span>
    </div>'''


def build_activation_html(link, username):
    """Build HTML content for activation email."""
    return f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;font-size:16px;color:#333;margin:0;padding:20px;">
    <div style="max-width:600px;margin:0 auto;">
        <div style="text-align:center;margin-bottom:30px;">
            {get_logo_html()}
        </div>
        <p>Dear {username},</p>
        <p>Thank you for registering with <strong>Videoflix</strong>. To complete your registration and verify your email address, please click the link below:</p>
        <p style="margin:30px 0;">
            <a href="{link}" style="background:#4D63D5;color:white;padding:14px 28px;text-decoration:none;border-radius:25px;font-weight:bold;display:inline-block;">Activate account</a>
        </p>
        <p>If you did not create an account with us, please disregard this email.</p>
        <p style="margin-top:30px;">Best regards,</p>
        <p>Your Videoflix Team.</p>
    </div>
</body>
</html>'''


def send_activation_email(user, uid, token):
    """Send account activation email to user."""
    link = f"{settings.FRONTEND_URL}/pages/auth/activate.html?uid={uid}&token={token}"
    username = user.email.split('@')[0]
    send_mail(
        subject='Confirm your email',
        message=f'Activate your account: {link}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=build_activation_html(link, username),
        fail_silently=False,
    )


def build_reset_html(link):
    """Build HTML content for password reset email."""
    return f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;font-size:16px;color:#333;margin:0;padding:20px;">
    <div style="max-width:600px;margin:0 auto;">
        <p>Hello,</p>
        <p>We recently received a request to reset your password. If you made this request, please click on the following link to reset your password:</p>
        <p style="margin:30px 0;">
            <a href="{link}" style="background:#4D63D5;color:white;padding:14px 28px;text-decoration:none;border-radius:25px;font-weight:bold;display:inline-block;">Reset password</a>
        </p>
        <p>Please note that for security reasons, this link is only valid for 24 hours.</p>
        <p>If you did not request a password reset, please ignore this email.</p>
        <p style="margin-top:30px;">Best regards,</p>
        <p>Your Videoflix team!</p>
        <div style="margin-top:40px;">
            {get_logo_html()}
        </div>
    </div>
</body>
</html>'''


def send_password_reset_email(user, uid, token):
    """Send password reset email to user."""
    link = f"{settings.FRONTEND_URL}/pages/auth/confirm_password.html?uid={uid}&token={token}"
    send_mail(
        subject='Reset your Password',
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