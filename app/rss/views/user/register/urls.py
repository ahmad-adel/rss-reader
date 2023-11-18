from django.urls import path

from .v1_0_0.view import RegisterView as RegisterView_v1_0_0

urlpatterns = [
    path(r'v1/user/register/', RegisterView_v1_0_0.as_view()),
]
