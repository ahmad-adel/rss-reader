from rest_framework import serializers


class PostReadStatusSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    is_read = serializers.BooleanField()
