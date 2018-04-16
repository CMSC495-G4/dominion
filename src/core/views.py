from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import LoginForm, SignupForm

def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        login(request, form.get_user())
        return redirect('index')
    else:
        return render(request, 'core/index.html', {'form': LoginForm()})

def about(request):
    return render(request, 'core/about.html')

def reset_password(request):
    return render(request, 'core/reset-password.html')

def rules(request):
    return render(request, 'core/rules.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})

def history(request):
    return HttpResponse('History placeholder')

def profile(request):
    return HttpResponse('Profile placeholder')

def play(request):
    return HttpResponse('Play placeholder')

def logout(request):
    auth_logout(request)
    return redirect('index')
