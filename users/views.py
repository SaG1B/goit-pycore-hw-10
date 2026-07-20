from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import RegisterForm

def signup_user(request):
    """
    Реєстрація нового користувача.
    """
    if request.user.is_authenticated:
        return redirect(to='quotes:root')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Ви успішно зареєструвалися!")
            return redirect(to='quotes:root')
    else:
        form = RegisterForm()
        
    return render(request, 'users/signup.html', {'form': form})

def login_user(request):
    """
    Авторизація (вхід) користувача.
    """
    if request.user.is_authenticated:
        return redirect(to='quotes:root')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Ласкаво просимо, {username}!")
                return redirect(to='quotes:root')
    else:
        form = AuthenticationForm()
        
    return render(request, 'users/login.html', {'form': form})

def logout_user(request):
    """
    Вихід з акаунту.
    """
    logout(request)
    messages.info(request, "Ви вийшли з системи.")
    return redirect(to='quotes:root')