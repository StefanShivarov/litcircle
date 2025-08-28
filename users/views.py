from django.shortcuts import render
from allauth.account.views import LoginView, SignupView


def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    return render(request, "landing.html")


class CustomLoginView(LoginView):
    template_name = 'sign_in.html'


class CustomSignupView(SignupView):
    template_name = 'sign_up.html'
