from rss.models import RSSFeed, RSSFeedFollow
from utils.interface_exception import InterfaceException


class ListInterface:
    def __init__(self, user) -> None:
        self.user = user

    def call(self) -> dict:
        """Removes the follow for the specified feed.

        Raises:
            InterfaceException: contains error message

        Returns:
            dict: contains:
                feeds (list): list of feed dicts
        """

        feed_list = self._get_feed_list()

        return {
            "feeds": feed_list,
        }

    def _get_feed_list(self) -> list[dict]:
        """Fetches data for each feed, and a flag to indicate whether follows them

        Returns:
            list[dict]: list of feed dicts 
        """
        feeds = RSSFeed.objects.all()

        feed_list = []
        for feed in feeds:
            is_followed = RSSFeedFollow.objects.filter(
                user=self.user, feed=feed).exists()
            feed_list.append({
                "pk": feed.pk,
                "title": feed.title,
                "description": feed.description,
                "updated": feed.updated.timestamp() if feed.updated else None,
                "is_followed": is_followed
            })

        return feed_list
