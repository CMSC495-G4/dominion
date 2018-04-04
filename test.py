import Player
import Game


def test1(arg):
    print(arg)


def take_turn():
    """Play a card, process each block while checking the input flag, if it is flagged, gather input and give it to the
    block"""

andy = Player.Player("P1")
jennifer = Player.Player("P2")

players = [andy, jennifer]
game = Game.Game(players)
game.select_kingdom_cards()
game.print_game_state()

