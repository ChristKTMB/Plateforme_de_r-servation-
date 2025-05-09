from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    """Formulaire d'inscription pour les utilisateurs"""
    phone = forms.CharField(max_length=20, required=False, label="Téléphone")
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date de naissance")
    address = forms.CharField(widget=forms.Textarea, required=False, label="Adresse")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone', 'user_type')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")