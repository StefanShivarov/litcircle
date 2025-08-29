from django.db import models
from users.models import Profile


class Book(models.Model):
    google_books_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=300)
    authors = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    thumbnail = models.URLField(blank=True)

    def __str__(self):
        return self.title
    

class Vote(models.Model):
    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE, related_name='votes')
    google_books_id = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['circle', 'google_books_id', 'profile'], name='unique_vote')
        ]

    def __str__(self):
        return f"{self.profile.user.username} voted for {self.book.title}"
    

class CircleReadBook(models.Model):
    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE, related_name='read_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['circle', 'book'], name='unique_circle_book')
        ]
