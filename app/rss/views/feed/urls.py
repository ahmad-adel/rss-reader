from .follow.urls import urlpatterns as follow_urlpatterns
from .list.urls import urlpatterns as list_urlpatterns
from .posts.urls import urlpatterns as posts_urlpatterns
from .refresh.urls import urlpatterns as refresh_urlpatterns
from .unfollow.urls import urlpatterns as unfollow_urlpatterns

urlpatterns = []

urlpatterns.extend(follow_urlpatterns)
urlpatterns.extend(list_urlpatterns)
urlpatterns.extend(posts_urlpatterns)
urlpatterns.extend(refresh_urlpatterns)
urlpatterns.extend(unfollow_urlpatterns)
