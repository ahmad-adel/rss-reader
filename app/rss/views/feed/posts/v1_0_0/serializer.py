from rest_framework import serializers


class PostsSerializer(serializers.Serializer):
    page = serializers.IntegerField(default=1)
    page_size = serializers.IntegerField(default=10)
    feed_pk = serializers.IntegerField(required=False)
    is_read = serializers.BooleanField(required=False)
    is_feed_followed = serializers.BooleanField(required=False)
