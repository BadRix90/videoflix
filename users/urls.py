"""URL configuration for user authentication."""
from django.urls import path
from .views import (
    register_view, activate_view, login_view, logout_view,
    token_refresh_view, password_reset_view, password_confirm_view
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('activate/<str:uidb64>/<str:token>/', activate_view, name='activate'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('token/refresh/', token_refresh_view, name='token_refresh'),
    path('password_reset/', password_reset_view, name='password_reset'),
    path('password_confirm/<str:uidb64>/<str:token>/', password_confirm_view, name='password_confirm'),
]