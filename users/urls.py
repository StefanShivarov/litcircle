from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


app_name = 'users'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signin', views.CustomLoginView.as_view(), name='signin'),
    path('signup', views.CustomSignupView.as_view(), name='signup'),
    path('signout', LogoutView.as_view(next_page='/'), name='signout')
]
