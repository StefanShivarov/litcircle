from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='First Name', required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', required=True)
    bio = forms.CharField(widget=forms.Textarea, label='Bio', required=False)
    image_file = forms.ImageField(label='Profile Picture', required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'bio')
        
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        profile = user.profile
        profile.bio = self.cleaned_data.get('bio', '')
        image_file = self.cleaned_data.get('image_file')
        if image_file:
            profile.image = image_file
        profile.save()

        return user
