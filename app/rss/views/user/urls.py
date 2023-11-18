from .login.urls import urlpatterns as login_urlpatterns
from .refresh.urls import urlpatterns as refresh_urlpatterns

urlpatterns = []

urlpatterns.extend(login_urlpatterns)
urlpatterns.extend(refresh_urlpatterns)
