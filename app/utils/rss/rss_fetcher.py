import feedparser

from datetime import datetime, timezone
from feedparser.util import FeedParserDict

class RSSFetcher:
    @classmethod
    def fetch_by_url(cls, url: str) -> dict:
        """Fetches RSS feed from the URL provided.
        Calls a validation function on the response.

        Args:
            url (str): RSS feed URL

        Returns:
            dict: validated response
        """
        result = feedparser.parse(url)
        validated_result = cls._validate(result)
        return validated_result

    @classmethod
    def _validate(cls, result: FeedParserDict) -> dict:
        """Check if the feed parsing result is successful and valid

        Args:
            result (FeedParserDict): returned by `feedparser.parse`

        Raises:
            Exception: with error message

        Returns:
            dict: validated result
        """

        result_dict = dict(result)

        if not "status" in result or result["status"] != 200:
            raise Exception("Invalid Feed Response (Status not 200)")

        if result["bozo"] != False:
            raise Exception("Invalid Feed Response (False Bozo)")

        # Convert time struct to datetime object
        updated_time_struct = result_dict["feed"]["updated_parsed"]
        updated_datetime = datetime(*updated_time_struct[:6]).replace(tzinfo=timezone.utc)

        return {
            "title": result_dict["feed"]["title"],
            "description": result_dict["feed"]["description"],
            "updated": updated_datetime,
            "entries": result["entries"],
        }

