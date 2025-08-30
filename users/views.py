from django.shortcuts import render, redirect
from allauth.account.views import LoginView, SignupView
from circles.models import Membership
from .forms import EditProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def home_view(request):
    if request.user.is_authenticated:
        memberships = Membership.objects.filter(
            profile=request.user.profile, status='approved'
        ).select_related('circle')
        return render(request, 'my_circles.html', {'memberships': memberships})
    return render(request, "landing.html")


@login_required
def profile_details(request):
    return render(request, 'profile_details.html', {'user': request.user})


@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('circles:my_circles')
    else:
        form = EditProfileForm(instance=profile, user=request.user)

    return render(request, 'edit_profile.html', {'form': form})


@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('users:home')
    return render(request, 'profile_details.html')


class CustomLoginView(LoginView):
    template_name = 'sign_in.html'


class CustomSignupView(SignupView):
    template_name = 'sign_up.html'
