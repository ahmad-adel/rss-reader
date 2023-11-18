from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include('rss.views.urls')),
    path('schema/', get_schema_view()),
]
