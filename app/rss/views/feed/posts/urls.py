from django.urls import path

from .v1_0_0.view import PostsView as PostsView_v1_0_0

urlpatterns = [
    path(r'v1/feed/posts/', PostsView_v1_0_0.as_view()),
]
