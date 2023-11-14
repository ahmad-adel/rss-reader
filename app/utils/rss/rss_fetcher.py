import feedparser

class RSSFetcher:
    @classmethod
    def fetch_by_url(cls, url: str) -> dict:
        result = feedparser.parse(url)
        return result
