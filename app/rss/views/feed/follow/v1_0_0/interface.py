from django.db import IntegrityError
from rss.models import RSSFeed, RSSFeedFollow
from utils.interface_exception import InterfaceException


class FollowInterface:
    def __init__(self, user) -> None:
        self.user = user

    def call(self, serializer_data: dict) -> dict:
        """Creates a RSSFeedFollow object if it does not already exist.

        Args:
            serializer_data (dict): includes:
                pk (int): feed pk.

        Raises:
            InterfaceException: contains error message

        Returns:
            dict: empty
        """
        pk = serializer_data['pk']

        try:
            feed = RSSFeed.objects.get(pk=pk)
        except RSSFeed.DoesNotExist:
            raise InterfaceException("Feed not found.")

        try:
            RSSFeedFollow.objects.create(user=self.user, feed=feed)
        except IntegrityError as ex:
            raise InterfaceException("Feed already followed.")

        return {}
