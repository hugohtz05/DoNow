from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse('productivity_tools:dashboard'))
        else:
            messages.info(request, 'Mot de passe ou pseudo incorrect')
    form = AuthenticationForm()        
    return render(request, 'user/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return render(request, 'productivity_tools/home.html')

def register_user(request):  
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect(reverse('productivity_tools:dashboard'))
    else:
        form = UserCreationForm()

    return render(request, "user/register.html", {'form': form})
