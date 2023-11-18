from django.urls import path

from .v1_0_0.view import UnfollowView as UnfollowView_v1_0_0

urlpatterns = [
    path(r'v1/feed/unfollow/', UnfollowView_v1_0_0.as_view()),
]
