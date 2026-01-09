"""Views for user authentication endpoints."""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import (
    RegisterSerializer, LoginSerializer,
    PasswordResetSerializer, PasswordConfirmSerializer
)
from .utils import (
    generate_token_data, send_activation_email, send_password_reset_email,
    set_auth_cookies, delete_auth_cookies, get_user_from_uidb64,
    verify_token, blacklist_refresh_token
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Register new user and send activation email."""
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    uid, token = generate_token_data(user)
    send_activation_email(user, uid, token)
    return Response(
        {'user': {'id': user.id, 'email': user.email}, 'token': token},
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def activate_view(request, uidb64, token):
    """Activate user account via email token."""
    user = get_user_from_uidb64(uidb64)
    if not user:
        return Response({'message': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)
    if not verify_token(user, token):
        return Response({'message': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
    user.is_active = True
    user.save()
    return Response({'message': 'Account successfully activated.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Authenticate user and set JWT cookies."""
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(
        username=serializer.validated_data['email'],
        password=serializer.validated_data['password']
    )
    if not user or not user.is_active:
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    refresh = RefreshToken.for_user(user)
    response = Response(
        {'detail': 'Login successful', 'user': {'id': user.id, 'username': user.email}},
        status=status.HTTP_200_OK
    )
    return set_auth_cookies(response, refresh)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    """Logout user and invalidate refresh token."""
    refresh_token = request.COOKIES.get('refresh_token')
    if not refresh_token:
        return Response({'detail': 'Refresh token missing.'}, status=status.HTTP_400_BAD_REQUEST)
    blacklist_refresh_token(refresh_token)
    response = Response(
        {'detail': 'Logout successful! All tokens will be deleted. Refresh token is now invalid.'},
        status=status.HTTP_200_OK
    )
    return delete_auth_cookies(response)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_refresh_view(request):
    """Refresh access token using refresh token cookie."""
    refresh_token = request.COOKIES.get('refresh_token')
    if not refresh_token:
        return Response({'detail': 'Refresh token missing.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        token = RefreshToken(refresh_token)
        response = Response(
            {'detail': 'Token refreshed', 'access': str(token.access_token)},
            status=status.HTTP_200_OK
        )
        response.set_cookie(
            'access_token', str(token.access_token),
            httponly=True, secure=False, samesite='Lax'
        )
        return response
    except Exception:
        return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_view(request):
    """Send password reset email."""
    serializer = PasswordResetSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=serializer.validated_data['email'])
        uid, token = generate_token_data(user)
        send_password_reset_email(user, uid, token)
    except User.DoesNotExist:
        pass
    return Response(
        {'detail': 'An email has been sent to reset your password.'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def password_confirm_view(request, uidb64, token):
    """Confirm password reset with new password."""
    serializer = PasswordConfirmSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = get_user_from_uidb64(uidb64)
    if not user:
        return Response({'detail': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)
    if not verify_token(user, token):
        return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(serializer.validated_data['new_password'])
    user.save()
    return Response({'detail': 'Your Password has been successfully reset.'}, status=status.HTTP_200_OK)