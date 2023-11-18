from django.db import IntegrityError
from rss.models import RSSFeed, RSSFeedFollow
from utils.interface_exception import InterfaceException


class UnfollowInterface:
    def __init__(self, user) -> None:
        self.user = user

    def call(self, serializer_data: dict) -> dict:
        """Removes the follow for the specified feed.

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
            follow = RSSFeedFollow.objects.get(feed__pk=pk, user=self.user)
        except RSSFeedFollow.DoesNotExist:
            raise InterfaceException("Feed not found or already not followed.")

        follow.delete()

        return {}
