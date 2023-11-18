from .follow.urls import urlpatterns as follow_urlpatterns
from .unfollow.urls import urlpatterns as unfollow_urlpatterns

urlpatterns = []

urlpatterns.extend(follow_urlpatterns)
urlpatterns.extend(unfollow_urlpatterns)
