from accounts.models import Token
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication


class APITokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            access_token_str = request.META.get('HTTP_AUTHORIZATION').split(' ')[-1]
            token = Token.objects.get(token=access_token_str, type='auth', is_active=True)
        except:
            return None

        user = token.user

        if token.is_expired():
            return None

        return (user, None)
