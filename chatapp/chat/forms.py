from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import *


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]


class RoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ["name"]

