from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class FanRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")