from django.urls import path

from .v1_0_0.view import ListView as ListView_v1_0_0

urlpatterns = [
    path(r'v1/feed/list/', ListView_v1_0_0.as_view()),
]
