from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import UserProfile

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
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})
