from rest_framework import serializers


class RefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=50)
