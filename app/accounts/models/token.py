from django.conf import settings
from django.db import models
from django.utils import timezone

import uuid
import datetime


def hex_uuid():
    return uuid.uuid4().hex


class Token(models.Model):
    TOKEN_TYPES = (
        ('auth', "Authentication"),
        ('refresh', "Refresh")
    )
    token = models.CharField(max_length=40, primary_key=True, default=hex_uuid)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    creation_time = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=40, choices=TOKEN_TYPES, default='auth')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.token

    def is_expired(self):
        is_expired = True

        if self.is_active:
            if self.type == 'auth':
                expiry = settings.AUTH_TOKEN_EXPIRY_SECONDS
                is_expired = self.creation_time + \
                    datetime.timedelta(seconds=expiry) < timezone.now()
            else:
                expiry = settings.REFRESH_TOKEN_EXPIRY_SECONDS
                is_expired = self.creation_time + \
                    datetime.timedelta(seconds=expiry) < timezone.now()

        return is_expired

    def revoke(self):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'
