from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from users.models import Profile
from .models import Circle, Membership
from books.models import Vote
from .forms import CircleForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from books.utils import fetch_google_book


@login_required
def create_circle(request):
    if request.method == 'POST':
        form = CircleForm(request.POST)
        if form.is_valid():
            circle = form.save(commit=False)
            circle.creator = request.user.profile
            circle.save()
            Membership.objects.create(profile=request.user.profile, circle=circle, is_owner=True, status='approved')
            return redirect('circles:circle_details', circle_id=circle.id)
    else:
        form = CircleForm()
    return render(request, 'create_circle.html', {'form': form})


@login_required
def request_to_join_circle(request, circle_id):
    circle = get_object_or_404(Circle, id=circle_id)
    membership, created = Membership.objects.get_or_create(
        profile=request.user.profile,
        circle=circle,
        defaults={'status': 'pending'}
    )

    if not created and membership.status != 'approved':
        membership.status = 'pending'
        membership.save()

    return redirect('circles:discover_circles')


@login_required
def cancel_request_to_join_circle(request, circle_id):
    circle = get_object_or_404(Circle, id=circle_id)
    membership = Membership.objects.filter(
        profile=request.user.profile,
        circle=circle,
        status='pending'
    ).first()

    if membership:
        membership.delete()

    return redirect('circles:discover_circles')


@login_required
def leave_circle(request, circle_id):
    circle = get_object_or_404(Circle, id=circle_id)
    membership = get_object_or_404(Membership, circle=circle, profile=request.user.profile)
    if not membership.is_owner:
        membership.delete()
    return redirect('circles:my_circles')


@login_required
def my_circles(request):
    memberships = Membership.objects.filter(profile=request.user.profile, status='approved')
    return render(request, 'my_circles.html', {'memberships': memberships})


@login_required
def circle_details(request, circle_id):
    circle = get_object_or_404(Circle, id=circle_id)
    members = Membership.objects.filter(circle=circle, status='approved').select_related('profile')

    is_member = members.filter(profile=request.user.profile).exists()
    if not is_member:
        raise PermissionDenied("You are not a member of this circle.")
    
    votes = Vote.objects.filter(circle=circle).select_related('profile')
    votes_with_books = []
    for vote in votes:
        book_data = fetch_google_book(vote.google_books_id)
        votes_with_books.append({
            'vote': vote,
            'book': book_data
        })

    return render(request, 'circle_details.html', {
        'circle': circle,
        'members': members,
        'votes': votes_with_books,
    })


@login_required
def delete_circle(request, circle_id):
    circle = get_object_or_404(Circle, id=circle_id)

    if request.user.profile != circle.creator:
        raise PermissionDenied("You do not have permission to delete this circle.")
    
    if request.method == 'POST':
        circle.delete()
        return redirect('circles:my_circles')
    
    return render(request, 'confirm_delete_circle.html', {'circle': circle})


@login_required
def search_circles(request):
    query = request.GET.get('q', '')

    approved_circle_ids = Membership.objects.filter(
        profile=request.user.profile,
        status='approved'
    ).values_list('circle_id', flat=True)

    pending_circle_ids = Membership.objects.filter(
        profile=request.user.profile,
        status='pending'
    ).values_list('circle_id', flat=True)

    circles = Circle.objects.exclude(id__in=approved_circle_ids)
    if query:
        circles = circles.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'discover_circles.html', {'circles': circles, 'query': query, 'pending_circle_ids': list(pending_circle_ids)})


@login_required
def add_user_to_circle(request, circle_id, user_id):
    circle = get_object_or_404(Circle, jd=circle_id)
    if circle.creator != request.user.profile:
        raise PermissionDenied("You do not have permission to add users to this circle.")
    
    query = request.GET.get('q', '')
    users = []
    if query:
        users = Profile.objects.filter(user__username__icontains=query).exclude(membership__circle=circle)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        profile_to_add = get_object_or_404(Profile, id=user_id)
        Membership.objects.create(profile=profile_to_add, circle=circle, status='approved')
        return redirect('circles:circle_details', circle_id=circle.id)
    
    return render(request, 'add_user_to_circle.html', {'circle': circle, 'users': users, 'query': query})


def __handle_membership_request(circle, action, membership_id):
    membership = get_object_or_404(Membership, id=membership_id, circle=circle, status='pending')
    if action == 'approve':
        membership.status = 'approved'
        membership.save()
    elif action == 'reject':
        membership.status = 'rejected'
        membership.save()
    else:
        raise ValueError("Invalid action")


def __add_user_to_circle(circle, profile_id):
    profile_to_add = get_object_or_404(Profile, id=profile_id)
    Membership.objects.update_or_create(profile=profile_to_add, circle=circle, status='approved')


def __remove_user_from_circle(circle, membership_id):
    membership = get_object_or_404(Membership, id=membership_id, circle=circle)
    if not membership.is_owner:
        membership.delete()


@login_required
def manage_circle_members(request, circle_id):
    circle = get_object_or_404(Circle, id=circle_id)
    if circle.creator != request.user.profile:
        return redirect('circles:circle_details', circle_id=circle.id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action in ['approve', 'reject']:
            __handle_membership_request(circle, action, request.POST.get('membership_id'))
        elif action == 'add':
            __add_user_to_circle(circle, request.POST.get('profile_id'))
        elif action == 'remove':
            __remove_user_from_circle(circle, request.POST.get('membership_id'))

        return redirect('circles:manage_circle_members', circle_id=circle.id)

    search_query = request.GET.get('q', '')
    search_user_profiles = []
    if search_query:
        search_user_profiles = Profile.objects.filter(user__username__icontains=search_query).exclude(
            membership__circle=circle
        )

    members = circle.memberships.filter(status='approved')
    pending_requests = circle.memberships.filter(status='pending')

    context = {
        'circle': circle,
        'pending_requests': pending_requests,
        'members': members,
        'search_results': search_user_profiles,
    }
    return render(request, 'manage_members.html', context)
