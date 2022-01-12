"""
Models for the users app
"""
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    """
    Custom user model to represent the users of the time tracking application
    """

    # Add any extra fields needed here

    def create_auth_token(self):
        """
        Create an auth token for this user
        """
        Token.objects.get_or_create(user=self)

    def __str__(self):
        return self.email
