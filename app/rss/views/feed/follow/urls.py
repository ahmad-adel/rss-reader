from django.urls import path

from .v1_0_0.view import FollowView as FollowView_v1_0_0

urlpatterns = [
    path(r'v1/feed/follow/', FollowView_v1_0_0.as_view()),
]
