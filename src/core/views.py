from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import redirect, render, reverse
from .forms import SignupForm, UserProfileForm
from .models import GameHistory


@login_required(login_url='login')
def index(request):
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


@login_required(login_url='login')
def play(request):
    return render(request, 'core/play.html')


@login_required(login_url='login')
def profile(request):

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserProfileForm()

    return render(request, 'core/profile.html', {'form': form})


class GameHistoryListView(generic.ListView):
    model = GameHistory
    context_object_name = 'game_history'

    def get_queryset(self):
        return GameHistory.objects.all()
