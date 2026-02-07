from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requis pour l'activation du compte.")

    class Meta:
        model = User
        fields = ('username', 'email')