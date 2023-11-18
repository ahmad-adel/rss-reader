from accounts.models import User, Token
from django.contrib.auth import authenticate
from utils.interface_exception import InterfaceException


class RegisterInterface:
    def call(self, serializer_data: dict) -> dict:
        """Register a user using their email and password.

        Args:
            serializer_data (dict): includes:
                email (str): user's email address.
                password (str): user's password.

        Raises:
            InterfaceException: contains error message

        Returns:
            dict: empty
        """
        email = serializer_data['email'].lower().strip()
        password = serializer_data['password']

        if User.objects.filter(email=email).exists():
            raise InterfaceException("Email already registered.")

        self._register_user(email, password)

        return {}
    
    def _register_user(self, email: str, password: str) -> None:
        """Create User and set password

        Args:
            email (str): user email
            password (str): user password
        """
        user = User.objects.create(email=email)

        user.set_password(password)
        user.save()
