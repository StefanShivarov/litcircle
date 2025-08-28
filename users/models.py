from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
