"""
All the service functions to add data to the db for the users app
"""
from .models import User


def create_user(username, email, password, first_name='', last_name='', **kwargs):
    """
    Create a new user with the provided data and generate an auth token for the
    created user

    Args:
        username (str): Unique username for the user
        email (str): Unique email for the user
        password (str): Password for the user
        first_name (str): First Name for the user (Optional)
        last_name (str): Last name for the user (Optional)

    Returns:
        User: Newly created user object
    """
    user = User.objects.create(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    user.set_password(password)
    user.save()

    # Create a JWT auth token a newly created user
    user.create_auth_token()
    return user
