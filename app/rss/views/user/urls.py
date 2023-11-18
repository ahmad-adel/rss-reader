from .login.urls import urlpatterns as login_urlpatterns
from .refresh_token.urls import urlpatterns as refresh_urlpatterns
from .register.urls import urlpatterns as register_urlpatterns

urlpatterns = []

urlpatterns.extend(login_urlpatterns)
urlpatterns.extend(refresh_urlpatterns)
urlpatterns.extend(register_urlpatterns)
