from django.urls import path

from .v1_0_0.view import RefreshView as RefreshView_v1_0_0

urlpatterns = [
    path(r'v1/user/refresh/', RefreshView_v1_0_0.as_view()),
]
