from django.shortcuts import render
from django.shortcuts import get_object_or_404
from circles.models import Circle
from .models import Message


def discussion_room(request, circle_id):
    circle = get_object_or_404(Circle, id=circle_id)
    messages = circle.messages.select_related('profile__user').all()
    return render(request, 'discussion.html', {
        'circle': circle,
        'messages': messages
    })
