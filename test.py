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
        print("BEGINNING OF TURN")
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
                while len(game.processQueue) != 0:
                    game.process_block()
                    if game.inputNeededFlag:
                        info = game.buffer
                        if info[0] == "Select":
                            player_selected_cards = False
                            while not player_selected_cards:
                                selectable_cards = ""
                                for card in info[1]:
                                    selectable_cards += card.get_name()
                                    selectable_cards += ", "
                                selected_cards = input("Choose " + info[2] + " cards from " + selectable_cards +
                                                       "and separate your choices with commas.")
                                selected_cards = [x.strip() for x in selected_cards.split(",")]

                                selected_real_cards = True
                                for user_selected_card in selected_cards:
                                    if user_selected_card not in selectable_cards:
                                        selected_real_cards = False
                                        print("That card was not in the possible selection.")
                                        break

                                if selected_real_cards:
                                    comparison_sign = info[2][1:3]

                                    num = info[2][3:4]
                                    if num == "H":  # Select no more cards than there are cards in the hand
                                        num = len(info[1])
                                    elif num == "D":  # Select enough cards that three cards are left unselected
                                        if len(info[1]) == 5:
                                            num = 2
                                        elif len(info[1]) == 4:
                                            num = 1
                                        else:
                                            num = 0
                                    else:
                                        num = int(num)

                                    if comparison_sign == "==":
                                        # Check to see if the amount of selected cards is equal to the constraint number
                                        if len(selected_cards) == num:
                                            game.buffer = selected_cards
                                            player_selected_cards = True
                                            game.inputNeededFlag = False
                                    elif comparison_sign == "<=":
                                        # Check to see if the amount of selected cards is less than the constraint number
                                        if len(selected_cards) <= num:
                                            game.buffer = selected_cards
                                            player_selected_cards = True
                                            game.inputNeededFlag = False

                        elif info[0] == "Question":
                            question_answered = False
                            while not question_answered:
                                print("Answer the following question with either Yes or No.")
                                answer = input(info[1])
                                print()
                                if answer == "Yes":
                                    game.playerAnswer = True
                                    question_answered = True
                                    game.inputNeededFlag = False
                                elif answer == "No":
                                    game.playerAnswer = False
                                    question_answered = True
                                    game.inputNeededFlag = False

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
                        if game.gain_cards(-1, card_name):
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
