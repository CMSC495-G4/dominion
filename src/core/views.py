import json
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.views import generic
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from .forms import SignupForm, UserProfileForm
from .models import Game


def json_response(data):
    response = HttpResponse(json.dumps(data))
    response['Content-Type'] = 'application/json'
    return response


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
def api_player(request, id):
    try:
        player = list(User.objects.all()
            .filter(id=id)
            .values('id', 'username'))[0]
        return json_response(player)
    except User.DoesNotExist:
        return json_response(None)


@login_required(login_url='login')
def api_games(request):
    games = list(Game.objects.all()\
        .values('id', 'player_1', 'player_2', 'winner'))

    return json_response(games)

@login_required(login_url='login')
def play_session(request, id):
    try:
        game = Game.objects.get(id=id)
        user = request.user

        # delete any other sessions the player might be in
        Game.objects.filter(
            Q(player_1=user) | Q(player_2=user),
            Q(winner=None),
            ~ Q(id=game.id)
        ).delete()

        if game.winner is None:
            return render(
                request,
                'core/play_session.html',
                {'game': game}
            )

        else:
            return redirect('index')
    except Game.DoesNotExist:
        return redirect('index')

@login_required(login_url='login')
def play(request):
    user = request.user

    # retrieve all games
    games = Game.objects.all()

    # try to find an open game (player_2 and winner are None)
    # if we have found one, then redirect the user
    # to that game
    try:
        open_game = games.get(player_2=None, winner=None)
        if open_game.player_1 == user:
            return render(request, 'core/play.html', {
                'game_id': open_game.id
            })

        else:
            open_game.player_2 = user
            open_game.save()
            return redirect('play_session', id=open_game.id)

    # otherwise, create a new game
    except Game.DoesNotExist:
        new_game = Game(player_1=user)
        new_game.save()
        return render(request, 'core/play.html', {
            'game_id': new_game.id
        })


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


class GameListView(generic.ListView):
    model = Game
    context_object_name = 'games'

    def get_queryset(self):
        return Game.objects.all()

