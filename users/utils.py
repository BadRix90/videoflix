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
    """Return Videoflix logo as embedded SVG."""
    return '''<img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAxIiBoZWlnaHQ9IjMyIiB2aWV3Qm94PSIwIDAgMjAxIDMyIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8ZyBjbGlwLXBhdGg9InVybCgjY2xpcDBfOTJfMjAxKSI+CjxwYXRoIGQ9Ik0wLjcxIDAuMDQ5OTg2NkMxLjA5IDAuMjI5OTg3IDEuNDcgMC40MTk5ODcgMS44NCAwLjU5OTk4N0MzLjYgMS40NDk5OSA1LjM1IDIuMzA5OTkgNy4xMSAzLjE1OTk5QzkuNTUgNC4zMzk5OSAxMS45OCA1LjUyOTk5IDE0LjQyIDYuNzA5OTlDMTYuNyA3LjgxOTk5IDE4Ljk4IDguOTI5OTkgMjEuMjYgMTAuMDNDMjMgMTAuODggMjQuNzQgMTEuNzcgMjYuNTQgMTIuNDlDMjUuMjYgMTIuMjMgMjMuOTEgMTIuNjIgMjIuNzMgMTMuMTJDMjEuNzEgMTMuNTYgMjAuNzMgMTQuMSAxOS43MiAxNC41N0MxOC42MiAxNS4wOCAxNy4zNSAxNS4wOCAxNi4yNCAxNC41OUw2LjIyIDEwLjE0QzIuNDQgOC40Njk5OSAwIDQuNjc5OTkgMCAwLjQ5OTk4N0MwIDAuMTI5OTg3IDAuMzggLTAuMTEwMDEzIDAuNzEgMC4wNDk5ODY2WiIgZmlsbD0idXJsKCNwYWludDBfbGluZWFyXzkyXzIwMSkiLz4KPHBhdGggZD0iTTMxLjMgMTcuMTdMNC4zIDMwLjM2TDEuMTEgMzEuOTJDMC42IDMyLjE3IDAgMzEuNzkgMCAzMS4yMlYzMC4xM0MwIDI3LjA4IDEuNjcgMjQuMyA0LjMgMjIuODhDNC40OCAyMi43OCA0LjY2IDIyLjcgNC44NCAyMi42MUwxOS40IDE2TDI0IDEzLjk0QzI0LjM0IDEzLjc5IDI0LjY5IDEzLjY3IDI1LjA1IDEzLjU4QzI1Ljc1IDEzLjQgMjYuNDcgMTMuMzQgMjcuMTkgMTMuNEMyNy45OCAxMy40NyAyOC43NSAxMy42OCAyOS40OCAxNC4wM0wzMS4zIDE0LjkxQzMyLjI0IDE1LjM3IDMyLjI0IDE2LjcyIDMxLjMgMTcuMTdaIiBmaWxsPSJ1cmwoI3BhaW50MV9saW5lYXJfOTJfMjAxKSIvPgo8cGF0aCBkPSJNNDguOTQ5OCAyMS43TDQ3LjQ2OTggMTguMzdMNDIuNzI5OCA3LjgzMDAxQzQxLjc3OTggNS43MDAwMSAzOS42Njk4IDQuMzIwMDEgMzcuMzM5OCA0LjMyMDAxSDM2LjU1OThDMzYuMTM5OCA0LjMyMDAxIDM1Ljg2OTggNC43NjAwMSAzNi4wNDk4IDUuMTMwMDFMNDYuNjI5OCAyNi45OUM0Ni45NDk4IDI3LjY3IDQ3LjkxOTggMjcuNjYgNDguMjQ5OCAyNi45OEw0OC44Nzk4IDI1LjY3QzQ5LjQ3OTggMjQuNDIgNDkuNTA5OCAyMi45NyA0OC45NDk4IDIxLjdaTTU4LjU2OTggNC4zMjAwMUM1NS41Nzk4IDQuMzIwMDEgNTIuODY5OCA2LjA5MDAxIDUxLjY1OTggOC44MzAwMUw0OC40Njk4IDE2LjA4QzQ4LjExOTggMTYuODkgNDguMTE5OCAxNy44IDQ4LjQ3OTggMTguNkM0OC44MTk4IDE5LjMzIDQ5LjIwOTggMjAuMDQgNDkuNTE5OCAyMC43OEM0OS44ODk4IDIxLjY0IDUwLjE1OTggMjIuNjIgNDkuOTc5OCAyMy41NEM1MC40ODk4IDIyLjI0IDUxLjEzOTggMjAuOTggNTEuNzM5OCAxOS43MkM1Mi41Mzk4IDE4LjA3IDUzLjMyOTggMTYuNDIgNTQuMTE5OCAxNC43N0M1NC45Njk4IDEzIDU1LjgxOTggMTEuMjQgNTYuNjY5OCA5LjQ3MDAxQzU3LjI3OTggOC4yMDAwMSA1Ny44ODk4IDYuOTMwMDEgNTguNDk5OCA1LjY2MDAxQzU4LjYzOTggNS4zOTAwMSA1OC43Njk4IDUuMTEwMDEgNTguODk5OCA0Ljg0MDAxQzU5LjAwOTggNC42MDAwMSA1OC44Mzk4IDQuMzIwMDEgNTguNTY5OCA0LjMyMDAxWk0xNjYuNiA0LjMyMDAxVjIyLjg0QzE2Ni42IDI1LjUxIDE2OC43NyAyNy42OCAxNzEuNDQgMjcuNjhWOS4xNjAwMUMxNzEuNDQgNi40OTAwMSAxNjkuMjcgNC4zMjAwMSAxNjYuNiA0LjMyMDAxWk0xNTQuNzMgMjNWOS4xNjAwMUMxNTQuNzMgNi40OTAwMSAxNTIuNTYgNC4zMjAwMSAxNDkuODkgNC4zMjAwMVYyNy42OEgxNjQuODRWMjNIMTU0LjczWk0xNDguMTMgOS4wMDAwMVY0LjMyMDAxSDEzMy4xOVYyNy42OEgxMzguMDJWMTguOTJIMTQ2LjMxVjE0LjI3SDEzOC4wMlY5LjAwMDAxSDE0OC4xM1pNMTE4Ljk4IDQuMDEwMDFDMTEyLjIgNC4wMTAwMSAxMDYuOTYgOS4yNTAwMSAxMDYuOTYgMTZDMTA2Ljk2IDIyLjc1IDExMi4xNyAyNy45OSAxMTguOTggMjcuOTlDMTI1Ljc5IDI3Ljk5IDEzMS4wNyAyMi43OCAxMzEuMDcgMTZDMTMxLjA3IDkuMjIwMDEgMTI1Ljc2IDQuMDEwMDEgMTE4Ljk4IDQuMDEwMDFaTTExOC45OCAyMy4yMkMxMTQuOTYgMjMuMjIgMTExLjkyIDIwLjE0IDExMS45MiAxNkMxMTEuOTIgMTEuODYgMTE0LjkgOC43ODAwMSAxMTguOTggOC43ODAwMUMxMjMuMDYgOC43ODAwMSAxMjYuMDggMTEuODUgMTI2LjA4IDE2QzEyNi4wOCAyMC4xNSAxMjMgMjMuMjIgMTE4Ljk4IDIzLjIyWk0xMDUuNzkgOC45NzAwMVY0LjMyMDAxSDkwLjUyOThWMjcuNjhIMTA1Ljc5VjIzLjAzSDk1LjM2OThWMTcuOThIMTA0LjU2VjEzLjYxSDk1LjM2OThWOC45NzAwMUgxMDUuNzlaTTc1LjQ0OTggNC4zMjAwMUg2Ny41MDk4VjI3LjY4SDc1LjQ0OThDODMuMTk5OCAyNy42OCA4OC4zODk4IDIzIDg4LjM4OTggMTZDODguMzg5OCA5LjAwMDAxIDgzLjE5OTggNC4zMjAwMSA3NS40NDk4IDQuMzIwMDFaTTc2LjEzOTggMjNINzIuMzM5OFY5LjAwMDAxSDc2LjEzOThDODAuNDM5OCA5LjAwMDAxIDgzLjQyOTggMTEuODUgODMuNDI5OCAxNkM4My40Mjk4IDIwLjE1IDgwLjQzOTggMjMgNzYuMTM5OCAyM1pNNTkuNTg5OCA0LjMyMDAxVjI3LjY4SDY0LjQyOThWOS4xNjAwMUM2NC40Mjk4IDYuNDkwMDEgNjIuMjU5OCA0LjMyMDAxIDU5LjU4OTggNC4zMjAwMVpNMTg2Ljg2IDE5LjA0TDE5NS4xNSAyNy41OUgxOTMuNjJDMTkwLjkgMjcuNTkgMTg4LjI5IDI2LjUgMTg2LjM4IDI0LjU3TDE4My45NyAyMi4xM0wxODMuNTMgMjEuNzRMMTgxLjkgMjMuMzlDMTc5Ljg2IDI1LjQ1IDE3OC4xIDI2LjgyIDE3NS4wNCAyNy4zNUMxNzQuMzMgMjcuNDcgMTczLjY5IDI2LjkyIDE3My42OSAyNi4yQzE3My42OSAyNS45IDE3My44MSAyNS42IDE3NC4wMyAyNS4zOEwxODAuNjYgMTguNzZMMTgwLjc1IDE4LjY5TDE4MC4xNCAxOC4wNkwxNzYuNjQgMTQuNTJIMTc2LjY1QzE3NC43IDEyLjU1IDE3My42IDkuODkwMDEgMTczLjYgNy4xMjAwMUMxNzMuNiA2LjU2MDAxIDE3NC4yOCA2LjI4MDAxIDE3NC42OCA2LjY4MDAxTDE4My42IDE1LjcxTDE4NC4yIDE1LjA5TDE4NS4yMyAxNC4wNUwxOTEuNDYgNy44MTAwMUMxOTMuNjMgNS42MzAwMSAxOTYuNTkgNC40MTAwMSAxOTkuNjcgNC40MTAwMUgyMDAuNjZMMTg3LjYgMTcuNUwxODcuMzggMTcuNzJMMTg2LjQ1IDE4LjY4TDE4Ni44NiAxOS4wNFoiIGZpbGw9InVybCgjcGFpbnQyX2xpbmVhcl85Ml8yMDEpIi8+CjwvZz4KPGRlZnM+CjxsaW5lYXJHcmFkaWVudCBpZD0icGFpbnQwX2xpbmVhcl85Ml8yMDEiIHgxPSIxMy4yNyIgeTE9IjE0Ljk2IiB4Mj0iMTMuMjciIHkyPSItMS4zNTA0ZS0wNSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPgo8c3RvcCBzdG9wLWNvbG9yPSIjMzU0N0ZGIi8+CjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzg5MDNGRiIvPgo8L2xpbmVhckdyYWRpZW50Pgo8bGluZWFyR3JhZGllbnQgaWQ9InBhaW50MV9saW5lYXJfOTJfMjAxIiB4MT0iLTAuOTQiIHkxPSIzMCIgeDI9IjMwLjA2IiB5Mj0iMTMuNSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPgo8c3RvcCBzdG9wLWNvbG9yPSIjODkwM0ZGIi8+CjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzM1NDdGRiIvPgo8L2xpbmVhckdyYWRpZW50Pgo8bGluZWFyR3JhZGllbnQgaWQ9InBhaW50Ml9saW5lYXJfOTJfMjAxIiB4MT0iMjUuMjc5OCIgeTE9IjI5Ljc1IiB4Mj0iMjA4Ljc0IiB5Mj0iMS44IiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CjxzdG9wIHN0b3AtY29sb3I9IiM4OTAzRkYiLz4KPHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjMzU0N0ZGIi8+CjwvbGluZWFyR3JhZGllbnQ+CjxjbGlwUGF0aCBpZD0iY2xpcDBfOTJfMjAxIj4KPHJlY3Qgd2lkdGg9IjIwMC42NiIgaGVpZ2h0PSIzMiIgZmlsbD0id2hpdGUiLz4KPC9jbGlwUGF0aD4KPC9kZWZzPgo8L3N2Zz4=" alt="Videoflix" style="height:32px;" />'''


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