from django.db import models
from django.contrib.auth.models import User


class GameHistory(models.Model):
    player_1 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='player_1')
    player_2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='player_2')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='winner')

