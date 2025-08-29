from django import forms
from .models import Circle


class CircleForm(forms.ModelForm):
    class Meta:
        model = Circle
        fields = ['name', 'description']

