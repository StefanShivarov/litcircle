from django.db import models
from users.models import Profile
from books.models import Book


class Circle(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_circles')
    created_at = models.DateTimeField(auto_now_add=True)
    selected_book = models.ForeignKey(Book, null=True, blank=True, on_delete=models.SET_NULL, related_name='in_circles')

    def __str__(self):
        return self.name
    

class Membership(models.Model):
    MEMBERSHIP_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name='memberships')
    is_owner = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=MEMBERSHIP_STATUS_CHOICES, default='pending')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['profile', 'circle'], name='unique_membership')
        ]
