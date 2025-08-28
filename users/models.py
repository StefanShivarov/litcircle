from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    social_image_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    @property
    def image_url(self):
        if self.image:
            return self.image.url
        if self.social_image_url:
            return self.social_image_url
        return '/static/images/default_profile.png'
