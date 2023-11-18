
import datetime

from django.utils import timezone
from rss.models import RSSFeed, RSSPost
from utils.mongo.rss_post_manager import RSSPostManagerInstance
from utils.rss.rss_fetcher import RSSFetcher


class RSSProcessor:
    def __init__(self, **args) -> None:
        self.RSSPostManagerInstance = RSSPostManagerInstance

    def process_feed(self, feed: RSSFeed) -> None:
        """Fetches data for a single feed.
        Initialize feed data if it was not fetched before.
        It also creates process the entries (posts) for this feed.
        If feed fetching raises an exception, retries with backoff are applied.

        Args:
            feed (RSSFeed): _description_
        """
        last_fetch = timezone.now()

        try:
            feed_data = RSSFetcher.fetch_by_url(feed.url)
        except Exception as ex:
            print(ex)
            self._implement_backoff(feed, last_fetch)
            return

        if feed.updated is None:
            self._initialize_feed_data(feed, feed_data)

        feed.set_updated(feed_data['updated'])

        self._process_feed_posts(feed, feed_data["entries"])

        # Set next refresh in 5 mins
        next_fetch = last_fetch + datetime.timedelta(minutes=5)
        feed.update_fetch_times(last_fetch, next_fetch)

    def _implement_backoff(self, feed: RSSFeed, last_fetch: datetime.datetime) -> None:
        """Implement backoff mechanism:
        - first failure: retry after 2 mins
        - second failure: retry after 5 mins
        - third failure: retry after 8 mins
        - fourth failure: no more retries (next_fetch is none)

        Args:
            feed (RSSFeed): _description_
            last_fetch (datetime.datetime): _description_
        """
        feed.last_fetch = last_fetch
        feed.failure_counter += 1

        if feed.failure_counter == 1:
            # 2 minute before next retry
            feed.next_fetch = last_fetch + datetime.timedelta(minutes=2)
        elif feed.failure_counter == 2:
            # 5 minute before next retry
            feed.next_fetch = last_fetch + datetime.timedelta(minutes=5)
        elif feed.failure_counter == 3:
            # 8 minute before next retry
            feed.next_fetch = last_fetch + datetime.timedelta(minutes=8)
        else:
            feed.failure_counter = 0
            feed.next_fetch = None

        feed.save()

    def _initialize_feed_data(self, feed: RSSFeed, feed_data: dict) -> None:
        """Set feed data fetched for the first time

        Args:
            feed (RSSFeed): feed object
            feed_data (dict): fetched from RSS service
        """
        feed.title = feed_data["title"]
        feed.description = feed_data["description"]
        feed.updated = feed_data["updated"]
        feed.save()

    def _process_feed_posts(self, feed: RSSFeed, entries: list[dict]) -> None:
        """ Feed posts are stored as RSSPost instances, and their data is stored in Mongo.
        Old posts are deleted from both databases first.

        Args:
            feed (RSSFeed): feed object
            entries (list[dict]): list of entries (posts) fetched from RSS service
        """

        # Delete posts that no longer exist
        to_be_deleted = self._find_deleted_posts(feed, entries)
        if to_be_deleted:
            RSSPost.objects.filter(feed=feed, pk__in=to_be_deleted).delete()
            self.RSSPostManagerInstance.bulk_delete(to_be_deleted)

        self._update_posts(feed, entries)

    def _update_posts(self, feed: RSSFeed, entries: list[dict]) -> None:
        """Update posts in both databases, either by updating existing posts or creating new ones

        Args:
            feed (RSSFeed): feed object
            entries (list[dict]): list of entries (posts) fetched from RSS service
        """
        for entry in entries:
            post, created = RSSPost.objects.get_or_create(
                feed=feed, guid=entry["id"])

            published = datetime.datetime(
                *entry["published_parsed"][:6]).replace(tzinfo=timezone.utc)
            post.set_published(published)

            if created:
                self.RSSPostManagerInstance.insert(post.pk, entry)
            else:
                self.RSSPostManagerInstance.update_one(post.pk, entry)

    def _find_deleted_posts(self, feed: RSSFeed, entries: list[dict]) -> list[int]:
        """Find deleted posts, which are the posts in the database but not fetched in the current refresh

        Args:
            feed (RSSFeed): feed object
            entries (list[dict]): list of entries (posts) fetched from RSS service

        Returns:
            list[int]: primary keys of posts to be deleted
        """
        new_guids = set([entry["id"] for entry in entries]
                        )     # set of guids, faster lookup
        old_posts = RSSPost.objects.filter(feed=feed).values("pk", "guid")

        to_be_deleted = []
        for post_data in old_posts:
            if post_data["guid"] not in new_guids:
                to_be_deleted.append(post_data["pk"])

        return to_be_deleted
