from django.http import JsonResponse
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny

from .serializer import RegisterSerializer
from .interface import RegisterInterface
from utils.interface_exception import InterfaceException


class RegisterView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)
    serializer_class = RegisterSerializer
    interface_class = RegisterInterface

    def post(self, request, *args, **kwargs):
        response = {}
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            response['message'] = "Please check the format of passed parameters and try again."
            response['errors'] = serializer.errors
            return JsonResponse(response, status=400)

        try:
            interface = self.interface_class()
            response = interface.call(serializer.validated_data)
            return JsonResponse(response, status=200)

        except InterfaceException as ex:
            response['message'] = ex.message
            return JsonResponse(response, status=422)
