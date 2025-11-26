from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

def get_tokens_for_user(user):
    """
    Returns access + refresh tokens for a given user.
    """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

def authenticate_user(email, password):
    """
    Authenticate a user using email and password.
    Returns user object or None.
    """
    user = authenticate(username=email, password=password)
    return user
