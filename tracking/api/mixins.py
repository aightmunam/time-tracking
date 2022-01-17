"""
Mixins for the tracking API views
"""
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED


class ReadWriteSerializerMixin:
    """
    Allows a read serializer for SAFE methods and write serializers
    for UNSAFE methods. Inheriting class must contain `read_serializer`
    and `write_serializer` attributes
    """

    def get_serializer_class(self):
        """
        Use the read serializer for Safe Methods and use the
        write serializer for the unsafe methods
        """
        if self.request.method in SAFE_METHODS:
            return self.read_serializer
        return self.write_serializer


class PostRequestMixin:
    """
    Override post request to send required serializer data. The APIview inheriting
    this mixin must implement `get_serializer_data` which will return the
    data to be sent to the write serializer
    """

    def post(self, request, *args, **kwargs):
        """
        Override the post method to create a contract associated with
        user id in the url
        """
        serializer = self.get_serializer(data=self.get_serializer_data())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
