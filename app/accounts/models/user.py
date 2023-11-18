from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        app_label = 'accounts'

    def save(self, *args, **kwargs):
        """If user is being created, email is assigned as username
        """
        if not self.pk and not self.is_superuser:
            self.username = self.email
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.email
