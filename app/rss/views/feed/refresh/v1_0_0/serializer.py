from rest_framework import serializers


class RefreshSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
