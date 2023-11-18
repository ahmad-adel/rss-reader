from .feed.urls import urlpatterns as feed_urlpatterns
from .user.urls import urlpatterns as user_urlpatterns

urlpatterns = []
urlpatterns.extend(feed_urlpatterns)
urlpatterns.extend(user_urlpatterns)
