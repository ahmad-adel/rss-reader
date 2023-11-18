from django.urls import path

from .v1_0_0.view import PostReadStatusView as PostReadStatusView_v1_0_0

urlpatterns = [
    path(r'v1/feed/post-read-status/', PostReadStatusView_v1_0_0.as_view()),
]
