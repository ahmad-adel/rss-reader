import mongomock

from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from rss.models import RSSFeed, RSSFeedFollow, RSSPost, RSSPostRead
from typing import Tuple, Union
from utils.mongo.rss_post_manager import RSSPostManagerInstance
from utils.interface_exception import InterfaceException


class PostsInterface:
    def __init__(self, user) -> None:
        self.user = user

    def call(self, serializer_data: dict) -> dict:
        """Fetch RSS posts, certain filter can apply.
        Results are paginated. Default page size = 10, default page number = 1.

        Args:
            serializer_data (dict): includes:
                page (int): page number.
                page_size (int): number of sessions per page.
                feed_pk (int): posts from a specific feed (nullable)
                is_read (bool): posts the user read before
                is_feed_followed (bool): posts of feeds the user follows

        Raises:
            InterfaceException: contains error message

        Returns:
            dict: contains:
                posts (list): list of dicts
                total_size (int): total number of posts in the DB
        """
        page = serializer_data['page']
        page_size = serializer_data['page_size']
        feed_pk = serializer_data.get('feed_pk')
        is_read = serializer_data.get('is_read')
        is_feed_followed = serializer_data.get('is_feed_followed')

        posts, total_size = self._query_posts(
            page, page_size, feed_pk, is_read, is_feed_followed)

        return {
            "posts": posts,
            "total_size": total_size
        }

    def _query_posts(
        self,
        page: int,
        page_size: int,
        feed_pk: Union[int, None],
        is_read: Union[bool, None],
        is_feed_followed: Union[bool, None]
    ) -> Tuple[list[dict], int]:
        """Fetch queried posts, ordered by descending publishing time

        Args:
            page (int): page number
            page_size (int): page size
            feed_pk (Union[int, None]): pk of a specified RSS feed (nullable)
            is_read (Union[bool, None]): only fetch posts read before (nullable)
            is_feed_followed (Union[bool, None]): only fetch posts from followed feeds (nullable)

        Raises:
            InterfaceException: contains error message

        Returns:
            Tuple[list[dict], int]: list of posts and the total number of posts in the DB
        """
        posts = RSSPost.objects.all().order_by("-published")
        read_post_pks = RSSPostRead.objects.filter(
            user=self.user).values_list("post__pk", flat=True)

        if feed_pk:
            if not RSSFeed.objects.filter(pk=feed_pk).exists():
                raise InterfaceException("Feed not found.")

            posts = posts.filter(feed__pk=feed_pk)

        if is_read:
            posts = posts.filter(pk__in=read_post_pks)

        if is_feed_followed:
            followed_feed_pks = RSSFeedFollow.objects.filter(
                user=self.user).values_list("feed__pk", flat=True)
            posts = posts.filter(feed__pk__in=followed_feed_pks)

        total_size = posts.count()

        posts = self._paginate(posts, page, page_size)

        post_data = self._fetch_post_data(posts, set(read_post_pks))

        return post_data, total_size

    def _paginate(self, posts: QuerySet, page: int, page_size: int) -> QuerySet:
        """Paginate the list of posts based on page number and page size

        Args:
            posts (QuerySet): posts queryset
            page (int): page number
            page_size (int): page size

        Returns:
            QuerySet: queryset of the posts in the specified page
        """
        paginated_data = Paginator(posts, page_size)
        try:
            current_page = paginated_data.page(page)
        except:
            current_page = paginated_data.page(1)

        return current_page.object_list

    def _fetch_post_data(self, posts: QuerySet, read_post_pks: set) -> list[dict]:
        """Fetch post data from Postgres and MongoDB

        Args:
            posts (QuerySet): queryset of posts to be fetched
            read_post_pks (set): posts read by the user

        Returns:
            list[dict]: each post's data
        """
        data_list = []

        read_post_pks_set = set(read_post_pks)

        for post in posts:
            post_data = RSSPostManagerInstance.fetch(post.pk)
            data_list.append({
                "pk": post.pk,
                "is_read": post.pk in read_post_pks_set,
                "data": post_data
            })

        return data_list
