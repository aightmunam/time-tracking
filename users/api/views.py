"""
All the api views for the users app
"""
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import (SAFE_METHODS, AllowAny, IsAdminUser,
                                        IsAuthenticated)

from users.models import User

from .serializers import RegisterUserSerializer, UserSerializer


class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    APIView to retrieve and update users. Only an admin
    or the user themselves can access their user object
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    model = User

    def get_queryset(self):
        """
        Filter users to only allow an admin or the user themselves access
        """
        if self.request.user.is_staff:
            return User.objects.all()

        return User.objects.filter(id=self.request.user.id)


class ListRegisterView(ListCreateAPIView):
    """
    APIView to register a new user
    """
    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Add a RegisterSerializer for POST request and UserSerializer for all
        GET calls
        """
        if self.request.method in SAFE_METHODS:
            return UserSerializer

        return RegisterUserSerializer

    def get_permissions(self):
        """
        Allow any one to register a new user but only allow an admin
        to list all the users
        """
        if self.request.method in SAFE_METHODS:
            return [IsAdminUser()]

        return [AllowAny()]
