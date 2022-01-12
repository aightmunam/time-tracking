"""
All the api views for the users app
"""
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

from users.models import User

from .permissions import IsOwnerOrAdmin
from .serializers import RegisterUserSerializer, UserSerializer


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    APIView to retrieve and update users. Only an admin
    or the user themselves can update their user object
    """
    queryset = User.objects.all()
    permission_classes = (IsOwnerOrAdmin,)
    serializer_class = UserSerializer


class ListRegisterView(generics.ListCreateAPIView):
    """
    APIView to register a new user
    """
    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Add a RegisterSerializer for POST request and UserSerializer for all
        GET calls
        """
        if self.request.method == 'GET':
            return UserSerializer

        return RegisterUserSerializer

    def get_permissions(self):
        """
        Allow any one to register a new user but only allow an admin
        to list all the users
        """
        if self.request.method == 'GET':
            return [IsAdminUser()]

        return [AllowAny()]
