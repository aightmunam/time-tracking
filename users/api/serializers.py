"""
Serializers for the users app
"""
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from users.models import User
from users.services import create_user


class UserSerializer(ModelSerializer):
    """
    Serializer for displaying a user
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', ]


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'confirm_password', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        """
        Check if both passwords are the same
        """
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields do not match."})

        return attrs

    def create(self, validated_data):
        """
        Create a user object with the validated data
        """
        return create_user(**validated_data)
