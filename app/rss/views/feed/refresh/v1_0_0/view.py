from django.http import JsonResponse
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from .serializer import RefreshSerializer
from .interface import RefreshInterface
from utils.interface_exception import InterfaceException
from utils.authentication.api_token import APITokenAuthentication


class RefreshView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [APITokenAuthentication,]
    parser_classes = (JSONParser,)
    serializer_class = RefreshSerializer
    interface_class = RefreshInterface

    def post(self, request, *args, **kwargs):
        response = {}
        user = request.user
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            response['message'] = "Please check the format of passed parameters and try again."
            response['errors'] = serializer.errors
            return JsonResponse(response, status=400)

        try:
            interface = self.interface_class(user)
            response = interface.call(serializer.validated_data)
            return JsonResponse(response, status=200)

        except InterfaceException as ex:
            response['message'] = ex.message
            return JsonResponse(response, status=422)
