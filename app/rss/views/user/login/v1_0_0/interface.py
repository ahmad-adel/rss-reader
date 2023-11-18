from accounts.models import User, Token
from django.contrib.auth import authenticate
from utils.interface_exception import InterfaceException


class LoginInterface:
    def call(self, serializer_data: dict) -> dict:
        """Authentication a user using their email and password.

        Args:
            serializer_data (dict): includes:
                email (str): user's email address.
                password (str): user's password.

        Raises:
            InterfaceException: contains error message

        Returns:
            dict: includes:
                access_token (str): user's access token.
                refresh_token (str): user's refresh token.
        """
        email = serializer_data['email'].lower().strip()
        password = serializer_data['password']

        try:
            user = User.objects.get(email=email)
        except:
            raise InterfaceException(
                "Authentication Failed. Please check your credentials.")

        if not user.check_password(password):
            raise InterfaceException(
                "Authentication Failed. Please check your credentials.")

        data = self._process_tokens(user)
        return data

    def _process_tokens(self, user: User) -> dict:
        """Revoke any old tokens, and generates a new pair.

        Args:
            user (User): authenticated user

        Returns:
            dict: contains access and refresh tokens
        """
        Token.objects.filter(user=user).update(is_active=False)

        access_token = Token.objects.create(user=user)
        refresh_token = Token.objects.create(user=user, type='refresh')

        return {
            'access_token': access_token.token,
            'refresh_token': refresh_token.token
        }
