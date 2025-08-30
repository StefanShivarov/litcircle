from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from .utils import search_google_books, fetch_google_book
from circles.models import Circle
from .models import Book, Vote, CircleReadBook


@login_required
def search_books_for_voting(request, circle_id):
    circle = get_object_or_404(Circle, id=circle_id)
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    results = []
    total_items = 0
    page_size = 20

    if query:
        results, total_items = search_google_books(query, page, page_size)
        already_read_in_circle = set(circle.read_books.values_list('book__google_books_id', flat=True))
        results = [book for book in results if book['google_books_id'] not in already_read_in_circle]

    total_pages = (total_items // page_size) + (1 if total_items % page_size else 0)
    page_numbers = range(1, total_pages + 1)

    context = {
        'circle': circle,
        'query': query,
        'results': results,
        'page': page,
        'total_pages': total_pages,
        'page_numbers': page_numbers,
    }

    return render(request, 'explore_books.html', context)


@login_required
@require_POST
def vote_for_book(request, circle_id, google_books_id):
    circle = get_object_or_404(Circle, id=circle_id)

    Vote.objects.update_or_create(
        circle=circle,
        profile=request.user.profile,
        defaults={'google_books_id': google_books_id}
    )

    return redirect('circles:circle_details', circle_id=circle.id)


@login_required
def circle_voting(request, circle_id):
    circle = get_object_or_404(Circle, id=circle_id)
    votes = circle.votes.select_related('profile')

    context = {
        'circle': circle,
        'votes': votes,
    }

    return render(request, 'explore_books.html', context)


@login_required
@require_POST
def select_book(request, circle_id, google_books_id):
    circle = get_object_or_404(Circle, id=circle_id)

    if circle.creator != request.user.profile:
        raise PermissionDenied("Only the circle owner can select the book.")
    
    book, created = Book.objects.get_or_create(
        google_books_id=google_books_id,
        defaults=fetch_google_book(google_books_id)
    )

    circle.selected_book = book
    circle.save()
    circle.votes.all().delete()
    return redirect('circles:circle_details', circle_id=circle.id)


@login_required
def finish_book(request, circle_id):
    circle = get_object_or_404(Circle, id=circle_id)

    if circle.creator != request.user.profile:
        raise PermissionDenied("Only the circle owner can finish the book.")

    if circle.selected_book:
        CircleReadBook.objects.get_or_create(circle=circle, book=circle.selected_book)
        circle.selected_book = None
        circle.save()

    return redirect('circles:circle_details', circle_id=circle.id)


