from django.contrib import admin
from .models import RSSFeed, RSSFeedFollow, RSSPost, RSSPostRead

admin.site.register(RSSFeed)
admin.site.register(RSSFeedFollow)
admin.site.register(RSSPost)
admin.site.register(RSSPostRead)
