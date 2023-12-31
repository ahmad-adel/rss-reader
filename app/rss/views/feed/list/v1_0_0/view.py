from django.http import JsonResponse
from rest_framework import generics, serializers
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from .interface import ListInterface
from .serializer import ListSerializer
from utils.interface_exception import InterfaceException
from utils.authentication.api_token import APITokenAuthentication


class ListView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [APITokenAuthentication,]
    serializer_class = ListSerializer
    parser_classes = (JSONParser,)
    interface_class = ListInterface

    def get(self, request, *args, **kwargs):
        response = {}
        user = request.user

        try:
            interface = self.interface_class(user)
            response = interface.call()
            return JsonResponse(response, status=200)

        except InterfaceException as ex:
            response['message'] = ex.message
            return JsonResponse(response, status=422)
