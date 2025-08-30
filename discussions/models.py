from django.db import models
from books.models import Book
from circles.models import Circle
from users.models import Profile


class Message(models.Model):
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name='messages')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.profile.user.username}: {self.content[:20]}"
