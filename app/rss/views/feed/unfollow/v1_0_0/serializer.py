from rest_framework import serializers


class UnfollowSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
