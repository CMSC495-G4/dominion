import Player
import Game

if __name__ == "__main__":
    p1 = Player.Player("John Doe")
    p2 = Player.Player("Jane Doe")

    players = [p1, p2]
    game = Game.Game(players)
    game.select_kingdom_cards()
    game.print_game_state()

    while not game.check_game_end():
        game.print_game_state()

        # Action phase
        while game.currentPlayer.get_current_actions() > 0 and game.currentPlayer.has_action_cards():
            print("You have " + str(game.currentPlayer.get_current_actions()) + " actions.")
            print(game.currentPlayer.get_action_cards())
            answer = input("Enter the name of the card you want to play or 'No' if you don't want to play any. ")
            if answer == "No":
                break
            else:
                num_of_actions = game.play_card(answer)  # Try to play their selection
                for i in range(num_of_actions):
                    game.process_block()
                game.currentPlayer.actions -= 1

                print("Middle of Action Phase ------")
                print(game.currentPlayer)
                print("-----------------------------------------")

        # Buy phase
        coins = game.currentPlayer.get_current_coins()
        while game.currentPlayer.get_current_buys() > 0:

            print("You have " + str(coins) + " coins and " + str(game.currentPlayer.get_current_buys()) + " buys.")
            answer = input("Do you want to buy a card? Enter 'Yes' if you do or 'No' if you don't want to buy any. ")
            if answer == "No":
                break
            else:
                available_cards = {}
                for card in game.supplyCards:
                    if card.get_cost() <= coins and game.supplyCards[card] > 0:
                        available_cards[card] = card.get_cost()

                print("Available cards:")
                for card in available_cards:
                    print(str(card) + " " + str(available_cards[card]) + "\t")
                card_name = input("Which card do you want to buy? Enter the name. ")

                print("|" + card_name + "|")
                print(available_cards)
                found = False
                for a_card in available_cards:
                    if a_card.get_name() == card_name:
                        found = True
                        if game.gain_cards(game.currentPlayer, card_name):
                            coins -= a_card.get_cost()
                            game.currentPlayer.buys -= 1
                            print(card_name + " bought.")
                        else:
                            print(card_name + " not found.")
                        break
                if not found:
                    print("That card is not available.")

        print(game.currentPlayer.name + "'s turn is over.")
        # Cleanup phase
        game.end_turn()
        print()


    game.print_game_state()

