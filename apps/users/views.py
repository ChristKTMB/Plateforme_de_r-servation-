from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm, LoginForm
from .models import UserProfile

from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Créer le profil utilisateur
            UserProfile.objects.create(
                user=user,
                birth_date=form.cleaned_data.get('birth_date'),
                address=form.cleaned_data.get('address')
            )
            login(request, user)
            messages.success(request, 'Compte créé avec succès!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Connexion réussie!')
                return redirect('home')
            else:
                messages.error(request, 'Identifiants invalides.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Vous êtes déconnecté.')
    return redirect('login')