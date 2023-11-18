from utils.rss.rss_processor import RSSProcessor
from rss.models import RSSFeed
from utils.interface_exception import InterfaceException


class RefreshInterface:
    def __init__(self, user) -> None:
        self.user = user

    def call(self, serializer_data: dict) -> dict:
        """Force refresh a feed by calling the RSSProcessor class.

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

        RSSProcessor().process_feed(feed)

        return {}
