from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import InviteCheckSerializer, InviteDoneSerializer


class InvitePlateCheck(GenericAPIView):
    serializer_class = InviteCheckSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class InviteDoneView(GenericAPIView):
    serializer_class = InviteDoneSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
