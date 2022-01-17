"""
Models for the users app
"""
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    """
    Custom user model to represent the users of the time tracking application
    """

    # Add any extra fields needed here

    def create_auth_token(self):
        """
        Create an auth token for this user
        """
        return RefreshToken.for_user(self)

    def get_tokens_for_user(self):
        """
        Return the JWT token for user
        """
        refresh = self.create_auth_token()

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def __str__(self):
        return self.email
