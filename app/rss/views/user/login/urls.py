from django.urls import path

from .v1_0_0.view import LoginView as LoginView_v1_0_0

urlpatterns = [
    path(r'v1/user/login/', LoginView_v1_0_0.as_view()),
]
