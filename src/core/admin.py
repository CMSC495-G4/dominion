from django.contrib import admin
from .models import GameHistory


@admin.register(GameHistory)
class GameHistoryAdmin(admin.ModelAdmin):
    list_display = ('player_1', 'player_2', 'winner')
