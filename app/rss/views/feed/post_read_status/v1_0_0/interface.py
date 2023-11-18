from django.db import IntegrityError
from rss.models import RSSPost, RSSPostRead
from utils.interface_exception import InterfaceException


class PostReadStatusInterface:
    def __init__(self, user) -> None:
        self.user = user

    def call(self, serializer_data: dict) -> dict:
        """Set the read status of a post. If it is not read, create a RSSPostRead record, else delete the record if found.

        Args:
            serializer_data (dict): includes:
                pk (int): post pk.
                is_read (bool): is the post read or not

        Raises:
            InterfaceException: contains error message

        Returns:
            dict: empty
        """
        pk = serializer_data['pk']
        is_read = serializer_data['is_read']

        try:
            post = RSSPost.objects.get(pk=pk)
        except RSSPost.DoesNotExist:
            raise InterfaceException("Post not found.")

        if is_read:
            RSSPostRead.objects.get_or_create(user=self.user, post=post)

        else:
            RSSPostRead.objects.filter(user=self.user, post=post).delete()

        return {}
