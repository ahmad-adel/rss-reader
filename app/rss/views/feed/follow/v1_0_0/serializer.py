from rest_framework import serializers


class FollowSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
