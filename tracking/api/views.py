"""
Views for the tracking app apis
"""
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import (SAFE_METHODS, IsAdminUser,
                                        IsAuthenticated)

from tracking.models import Contract, Project, Timelog
from tracking.selectors import get_contracts_for_user, get_timelogs_for_user

from .mixins import PostRequestMixin, ReadWriteSerializerMixin
from .permissions import IsAdminOrOwner
from .serializers import (ContractReadSerializer, ContractWriteSerializer,
                          ProjectSerializer, TimelogReadSerializer,
                          TimelogWriteSerializer)


class ProjectListCreateAPIView(ListCreateAPIView):
    """
    Allow authenticated users to GET all projects. Allow only admins to
    create new Projects.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        """
        Allow only admins to add new Projects
        """
        if self.request.method not in SAFE_METHODS:
            return [IsAdminUser()]

        return [IsAuthenticated()]


class ProjectRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Allow users to GET a single Project. Allows only admins
    to update or delete a project
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAdminUser,)

    def get_permissions(self):
        """
        Allow only admins to update/delete Projects
        """
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]

        return [IsAdminUser()]


class ContractListAPIView(ListAPIView):
    """
    APIView to list contracts
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ContractReadSerializer
    filterset_fields = ['user', 'project']

    def get_queryset(self):
        """
        Show all contracts for an admin and show the user specific contracts otherwise
        """
        if self.request.user.is_staff:
            return Contract.objects.all()
        return get_contracts_for_user(self.request.user.id)


class UserContractListCreateAPIView(
    ReadWriteSerializerMixin,
    PostRequestMixin,
    ListCreateAPIView
):
    """
    List all the contracts for the given user id. Only accessible by the
    user themselves or the admin
    """

    permission_classes = (IsAdminOrOwner,)
    read_serializer = ContractReadSerializer
    write_serializer = ContractWriteSerializer
    filterset_fields = ['project']

    def get_serializer_data(self):
        """
        Get the data to be sent to the write serializer. Passes the Project ID
        from the URL to the serializer data dict
        """
        data = self.request.data.copy()
        data['user'] = self.kwargs['user_id']
        return data

    def get_queryset(self):
        """
        Filter the contract based on the user_id in the url
        """
        return get_contracts_for_user(self.kwargs['user_id'])


class ContractRetrieveUpdateDestroyAPIView(
    ReadWriteSerializerMixin,
    RetrieveUpdateDestroyAPIView
):
    """
    Allow users to retrieve, update or delete a single contract
    that belongs to them. Admins have access to all the contracts.
    """

    permission_classes = (IsAdminOrOwner,)
    model = Contract
    read_serializer = ContractReadSerializer
    write_serializer = ContractWriteSerializer

    def get_serializer_class(self):
        """
        Use the read serializer for Safe Methods and use the
        write serializer for the unsafe methods
        """
        if self.request.method in SAFE_METHODS:
            return ContractReadSerializer
        return ContractWriteSerializer

    def get_queryset(self):
        """
        Show all the objects belonging to the given user id. If the
        user is an admin, show all objects.
        """
        if self.request.user.is_staff:
            return Contract.objects.all()
        return get_contracts_for_user(self.request.user.id)


class TimelogListAPIView(ListAPIView):
    """
    APIView to list Timelogs
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = TimelogReadSerializer
    queryset = Timelog.objects.all()
    filterset_fields = ['contract', 'date']

    def get_queryset(self):
        """
        Show all logs of all users for an admin and show the user specific logs otherwise
        """
        if self.request.user.is_staff:
            return Timelog.objects.all()
        return get_timelogs_for_user(self.request.user.id)


class UserTimelogListCreateAPIView(
    ReadWriteSerializerMixin,
    PostRequestMixin,
    ListCreateAPIView
):
    """
    List all the contracts for the given user id. Only accessible by the
    user themselves or the admin
    """

    permission_classes = (IsAdminOrOwner,)
    read_serializer = TimelogReadSerializer
    write_serializer = TimelogWriteSerializer
    filterset_fields = ['contract', 'date']

    def get_serializer_data(self):
        """
        Get the data to be sent to the write serializer. Passes the Project ID
        from the URL to the serializer data dict
        """
        data = self.request.data.copy()
        data['user'] = self.kwargs['user_id']
        return data

    def get_queryset(self):
        """
        Filter to show only the given user id contracts
        """
        return get_timelogs_for_user(self.kwargs['user_id'])


class TimelogRetrieveUpdateDestroyAPIView(
    ReadWriteSerializerMixin,
    RetrieveUpdateDestroyAPIView
):
    """
    APIView to get, update or delete a single timelog by ID
    """

    permission_classes = (IsAdminOrOwner,)
    read_serializer = TimelogReadSerializer
    write_serializer = TimelogWriteSerializer

    def get_queryset(self):
        """
        Show all the objects belonging to the given user id. If the
        user is an admin, show all objects.
        """
        if self.request.user.is_staff:
            return Timelog.objects.all()
        return get_timelogs_for_user(self.request.user.id)
