from django.contrib.auth import login
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import redirect, render, reverse
from .forms import LoginForm, SignupForm
from .models import GameHistory


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'core/index.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})


def about(request):
    return render(request, 'core/about.html')


def rules(request):
    return render(request, 'core/rules.html')


def history(request):
    return HttpResponse('History placeholder')


def profile(request):
    return HttpResponse('Profile placeholder')


def play(request):
    return HttpResponse('Play placeholder')


class GameHistoryListView(generic.ListView):
    model = GameHistory

