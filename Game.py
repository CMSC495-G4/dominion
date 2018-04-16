import Player
import Card
import random

# Replace with database?
allKingdomCards = [Card.ActionCard("Cellar", 2, "Action", "+1 Action, Discard any number of cards. +1 Card per card "
                                                          "discarded."),
                   Card.ActionCard("Chapel", 2, "Action", "Trash up to 4 cards from your hand."),
                   Card.ReactionCard("Moat", 2, "Action-Reaction", "+2 Cards", "When another player plays an Attack "
                                                                               "card, you may reveal this from your "
                                                                               "hand. If you do, you are unaffected "
                                                                               "by that Attack."),
                   Card.ActionCard("Chancellor", 3, "Action", "+2 Coins, You may immediately put your deck into your "
                                                              "discard pile."),
                   Card.ActionCard("Village", 3, "Action", "+1 Card, +2 Actions."),
                   Card.ActionCard("Woodcutter", 3, "Action", "+1 Buy, +2 Coins."),
                   Card.ActionCard("Workshop", 3, "Action", "Gain a card costing up to 4 Coins."),
                   Card.ActionCard("Bureaucrat", 4, "Action-Attack", "Gain a silver card; put it on top of your deck. "
                                                                     "Each other player reveals a Victory card from "
                                                                     "his hand and puts it on his deck (or reveals a "
                                                                     "hand with no Victory cards)."),
                   Card.ActionCard("Feast", 4, "Action", "Trash this card. Gain a card costing up to 5 Coins."),
                   Card.VictoryCard("Gardens", 4, "Victory", "Variable, Worth 1 Victory for every 10 cards in your "
                                                             "deck (rounded down)."),
                   Card.ActionCard("Militia", 4, "Action-Attack", "+2 Coins, Each other player discards down to 3 "
                                                                  "cards in his hand."),
                   Card.ActionCard("Moneylender", 4, "Action", "Trash a Copper from your hand. If you do, +3 Coins."),
                   Card.ActionCard("Remodel", 4, "Action", "Trash a card from your hand. Gain a card costing up to 2 "
                                                           "Coins more than the trashed card."),
                   Card.ActionCard("Smithy", 4, "Action", "+3 Cards."),
                   Card.ActionCard("Spy", 4, "Action-Attack", "+1 Card +1 Action Each player (including you) reveals "
                                                              "the top card of his deck and either discards it or "
                                                              "puts it back, your choice."),
                   Card.ActionCard("Thief", 4, "Action-Attack", "Each other player reveals the top 2 cards of his "
                                                                "deck. If they revealed any Treasure cards, "
                                                                "they trash one of them that you choose. You may gain "
                                                                "any or all of these trashed cards. They discard the "
                                                                "other revealed cards."),
                   Card.ActionCard("Throne Room", 4, "Action", "Choose an Action card in your hand. Play it twice."),
                   Card.ActionCard("Council Room", 5, "Action", "+4 Cards, +1 Buy, Each other player draws a card."),
                   Card.ActionCard("Festival", 5, "Action", "+2 Actions, +1 Buy, +2 Coins."),
                   Card.ActionCard("Laboratory", 5, "Action", "+2 Cards, +1 Action."),
                   Card.ActionCard("Library", 5, "Action", "Draw until you have 7 cards in hand. You may set aside "
                                                           "any Action cards drawn this way, as you draw them; "
                                                           "discard the set aside cards after you finish drawing."),
                   Card.ActionCard("Market", 5, "Action", "+1 Card, +1 Action, +1 Buy, +1 Coin."),
                   Card.ActionCard("Mine", 5, "Action", "Trash a Treasure card from your hand. Gain a Treasure card "
                                                        "costing up to 3 Coins more; put it into your hand."),
                   Card.ActionCard("Witch", 5, "Action-Attack", "+2 Cards, Each other player gains a Curse card."),
                   Card.ActionCard("Adventurer", 6, "Action", "Reveal cards from your deck until you reveal 2 "
                                                              "Treasure cards. Put those Treasure cards into your "
                                                              "hand and discard the other revealed cards."),
                   Card.TreasureCard("Copper", 0, "Treasure", 1),
                   Card.TreasureCard("Silver", 3, "Treasure", 2),
                   Card.TreasureCard("Gold", 6, "Treasure", 3),
                   Card.VictoryCard("Curse", 0, "Victory", -1),
                   Card.VictoryCard("Estate", 2, "Victory", 1),
                   Card.VictoryCard("Duchy", 5, "Victory", 3),
                   Card.VictoryCard("Province", 8, "Victory", 6)]

CURRENT_PLAYER = -1


class Game:
    def __init__(self, players):
        self.supplyCards = {}
        self.players = players
        self.trash = []
        self.playArea = []
        self.processQueue = []
        self.currentPlayer = random.choice(players)

        self.buffer = [""]  # The way of communicating with the player. Input/output of the game is set to the buffer
        self.playerAnswer = False  # The player's response to a question. Used for decisions that the game can't make
        self.playerCompletedAction = False  # If the last block completed. Used for chained actions
        self.check = False  # Used for internal checks on the type of card a card is (Only set by check_played_card)
        self.playersEligibleForAttack = []  # A list of players that do not have a Moat. Populated after each attack
        self.currentMoves = 0  # Amount of times a card has been moved per card process. Used for Adventurer's effect
        self.inputNeededFlag = False  # Signal to the function controlling the game that it requires outside input

        self.allKingdomActionCards = {
            "Cellar": [[self.add_actions, 1],
                       [self.select_cards, CURRENT_PLAYER, "Hand", "#<=H"],
                       [self.discard_cards, CURRENT_PLAYER, "Hand"],
                       [self.draw_cards, "Buffer"]],

            "Chapel": [[self.select_cards, CURRENT_PLAYER, "Hand", "#<=4"],
                       [self.trash_cards, CURRENT_PLAYER, "", "Hand"]],

            "Moat": [[self.draw_cards, 2]],

            "Chancellor": [[self.add_coins, 2],
                           [self.ask_player, "Do you want to shuffle your deck?"],
                           [self.shuffle_deck, True]],

            "Village": [[self.draw_cards, 1],
                        [self.add_actions, 2]],

            "Woodcutter": [[self.add_buys, 1],
                           [self.add_coins, 2]],

            "Workshop": [[self.select_cards, -1, "Supply", "#==1 $<=4"],
                         [self.gain_cards, CURRENT_PLAYER, ""]],

            "Bureaucrat": [[self.gain_cards, CURRENT_PLAYER, "Silver", "Top of Deck"],
                           [self.poll_players_for_attack],
                           [self.select_cards, 0, "Hand", "#==1 Victory"],
                           [self.move_cards, 0, "Hand", "Top of Deck", "Buffer"],
                           [self.select_cards, 1, "Hand", "#==1 Victory"],
                           [self.move_cards, 1, "Hand", "Top of Deck", "Buffer"],
                           [self.select_cards, 2, "Hand", "#==1 Victory"],
                           [self.move_cards, 2, "Hand", "Top of Deck", "Buffer"]],

            "Feast": [[self.trash_cards, -1, ["Feast"], "Play Area"],
                      [self.select_cards, -1, "Supply", "#==1 $<=5"],
                      [self.gain_cards, CURRENT_PLAYER, "", "Play Area", True]],

            "Militia": [[self.add_coins, 2],
                        [self.poll_players_for_attack],
                        [self.select_cards, 0, "Hand", "#==D"],
                        [self.discard_cards, 0, "Hand"],
                        [self.select_cards, 1, "Hand", "#==D"],
                        [self.discard_cards, 1, "Hand"],
                        [self.select_cards, 2, "Hand", "#==D"],
                        [self.discard_cards, 2, "Hand"]],

            "Moneylender": [[self.trash_cards, CURRENT_PLAYER, ["Copper"], "Hand"],
                            [self.add_coins, 3, True]],

            "Remodel": [[self.select_cards, CURRENT_PLAYER, "Hand", "#==1"],
                        [self.trash_cards, CURRENT_PLAYER, "", "Hand"],
                        [self.select_cards, CURRENT_PLAYER, "Supply", "#==1 $<=T+2", True],
                        [self.gain_cards, CURRENT_PLAYER, ""]],

            "Smithy": [[self.draw_cards, 3]],

            "Spy": [[self.draw_cards, 1],
                    [self.add_actions, 1],
                    [self.poll_players_for_attack],
                    [self.reveal_top_cards, CURRENT_PLAYER, 1],
                    [self.ask_player, "Do you want the to discard the card?"],
                    [self.discard_cards, CURRENT_PLAYER, "Top of Deck", True],
                    [self.reveal_top_cards, 0, 1],
                    [self.ask_player, "Do you want the player to discard the card?", "", 0],
                    [self.discard_cards, 0, "Top of Deck", True],
                    [self.reveal_top_cards, 1, 1],
                    [self.ask_player, "Do you want the player to discard the card?", "", 1],
                    [self.discard_cards, 1, "Top of Deck", True],
                    [self.reveal_top_cards, 2, 1],
                    [self.ask_player, "Do you want the player to discard the card?", "", 2],
                    [self.discard_cards, 2, "Top of Deck", True]],

            "Thief": [[self.poll_players_for_attack],
                      [self.put_cards_play_area, 0, 2],
                      [self.select_cards, CURRENT_PLAYER, "0 Play Area", "#<=1 Treasure", True],
                      [self.trash_cards, 0, "", "Play Area", True],
                      [self.ask_player, "Do you want to gain the trashed card?", "Action", 0],
                      [self.give_trashed_cards, True],
                      [self.put_cards_play_area, 1, 2],
                      [self.select_cards, CURRENT_PLAYER, "1 Play Area", "#<=1 Treasure", True],
                      [self.trash_cards, 1, "", "Play Area", True],
                      [self.ask_player, "Do you want to gain the trashed card?", "Action", 1],
                      [self.give_trashed_cards, True],
                      [self.put_cards_play_area, 2, 2],
                      [self.select_cards, CURRENT_PLAYER, "2 Play Area", "#<=1 Treasure", True],
                      [self.trash_cards, 2, "", "Play Area", True],
                      [self.ask_player, "Do you want to gain the trashed card?", "Action", 2],
                      [self.give_trashed_cards, True]],

            "Throne Room": [[self.select_cards, CURRENT_PLAYER, "Hand", "#==1 Action"],
                            [self.add_card_blocks, "Buffer", False, False, True],
                            [self.add_card_blocks, "Buffer", False, False, True]],

            "Council Room": [[self.draw_cards, 1, 1],
                             [self.draw_cards, 1, 2],
                             [self.draw_cards, 1, 3],
                             [self.draw_cards, 4, 0]],

            "Festival": [[self.add_actions, 2],
                         [self.add_buys, 1],
                         [self.add_coins, 2]],

            "Laboratory": [[self.draw_cards, 2],
                           [self.add_actions, 1]],

            # The check is testing to see if the card is an action card, if it is, self.check is true
            # The player is being asked if they want to set aside the Action card, if they do, self.playerAnswer is true
            # Therefore, move the card to the hand if they say not to set it aside or if the card is not an action
            "Library": [[self.put_cards_play_area, CURRENT_PLAYER, 1, True],
                        [self.check_played_card, "Action", True],
                        [self.ask_player, "Do you want to set aside the Action card?", "Function"],
                        [self.move_cards, CURRENT_PLAYER, "Play Area", "Hand", "Most Recent Played", 100, True, True],
                        [self.add_card_blocks, "Library", False, True]],

            "Market": [[self.draw_cards, 1],
                       [self.add_actions, 1],
                       [self.add_buys, 1],
                       [self.add_coins, 1]],

            "Mine": [[self.select_cards, CURRENT_PLAYER, "Hand", "#==1 Treasure"],
                     [self.trash_cards, CURRENT_PLAYER, "", "Hand"],
                     [self.select_cards, CURRENT_PLAYER, "Supply", "#==1 $<=T+3 Treasure", True],
                     [self.gain_cards, CURRENT_PLAYER, "", "Play Area", True]],

            "Witch": [[self.draw_cards, 2],
                      [self.poll_players_for_attack],
                      [self.gain_cards, 0, "Curse"],
                      [self.gain_cards, 1, "Curse"],
                      [self.gain_cards, 2, "Curse"]],

            "Adventurer": [[self.put_cards_play_area, CURRENT_PLAYER, 1],
                           [self.check_played_card, "Treasure", True],
                           [self.move_cards, CURRENT_PLAYER, "Play Area", "Hand", "Most Recent Played", True],
                           [self.add_card_blocks, "Adventurer", True]]
        }

    def get_supply_cards(self):
        return self.supplyCards

    def select_kingdom_cards(self):
        """Randomly generate 10 numbers to select 10 Kingdom cards
        Add those cards to the supply with the appropriate amount
        Add the Treasure and Victory cards to the supply"""

        chosen = []
        while len(chosen) != 25:  # CHANGE THIS TO 10 WHEN DONE DEBUGGING
            print(len(chosen))
            rand_card = random.randint(0, 24)
            if rand_card not in chosen:
                self.supplyCards[allKingdomCards[rand_card]] = 10  # Add all Kingdom cards to supply
                chosen.append(rand_card)
        self.supplyCards[allKingdomCards[25]] = 60 - (len(self.players) * 7)  # Add Copper cards to supply
        self.supplyCards[allKingdomCards[26]] = 40  # Add Silver cards to supply
        self.supplyCards[allKingdomCards[27]] = 30  # Add Gold cards to supply
        self.supplyCards[allKingdomCards[28]] = 30  # Add Curse cards to supply
        self.supplyCards[allKingdomCards[29]] = 24 - (len(self.players) * 3)  # Add Estate cards to supply
        self.supplyCards[allKingdomCards[30]] = 12  # Add Duchy cards to supply
        self.supplyCards[allKingdomCards[31]] = 12  # Add Province cards to supply

    def play_card(self, name):
        """Add the individual blocks of actions to the queue
        Move the card from the player's hand to the play area
        Return the amount of actions found"""
        num_of_actions = self.add_card_blocks(name)
        self.move_cards(CURRENT_PLAYER, "Hand", "Play Area", name)
        self.playerCompletedAction = False  # CHANGE OTHER METHODS TO CHANGE THIS TO TRUE WHEN THEY COMPLETE
        return num_of_actions

    def add_card_blocks(self, name, check_moves=False, check_hand=False, check_action=False):
        """Query database for list of actions
        Split actions into individual actions
        Add each action with the appropriate arguments to the queue
        Return the amount of actions found"""
        if check_moves:
            # It checks for 3 moves because one move is used for when the Action card is moved from the hand to the
            #   play area.
            if not self.playerCompletedAction or 3 == self.currentMoves:
                return
        if check_hand and 7 <= self.currentPlayer.get_hand_size():
            return
        if check_action and not self.playerCompletedAction:
            return

        if name == "Buffer":
            name = self.buffer

        actions = self.allKingdomActionCards[name]
        for action in actions:
            self.processQueue.append(action)
        return len(actions)

    def process_block(self):
        """Process the first block in the queue."""
        block = self.processQueue.pop(0)

        if len(block) == 1:
            return block[0]()
        elif len(block) == 2:
            return block[0](block[1])
        elif len(block) == 3:
            return block[0](block[1], block[2])
        elif len(block) == 4:
            return block[0](block[1], block[2], block[3])
        elif len(block) == 5:
            return block[0](block[1], block[2], block[3], block[4])
        elif len(block) == 6:
            return block[0](block[1], block[2], block[3], block[4], block[5])
        elif len(block) == 7:
            return block[0](block[1], block[2], block[3], block[4], block[5], block[6])
        elif len(block) == 8:
            return block[0](block[1], block[2], block[3], block[4], block[5], block[6], block[7])

    #
    # Block Functions

    # amount - The amount of cards to draw
    # player_offset - Specifies how many players to go past the current player
    def draw_cards(self, amount, player_offset=0):
        """Draw cards from the specified player's deck and add them to their hand
        Return the specific cards drawn"""

        if amount == "Buffer":
            amount = len(self.buffer)

        if player_offset == 0:
            return self.currentPlayer.draw_card(amount)
        else:
            if len(self.players) > player_offset:
                self.players[(self.players.index(self.currentPlayer) + player_offset) % len(self.players)].draw_card(amount)

    # player_offset - Specifies how many players to go past the current player
    def reveal_top_cards(self, player_offset, amount):
        """If player object is an array, check to see if the array is long enough for the player to exist
        Set the buffer to the card objects so that discard_cards can find the names
        Return the card object (CHANGE IF NEEDED, DOES NOT AFFECT INTERNAL FUNCTIONS)
        Revealed cards are NOT moved, the card object is merely returned"""

        player = self.currentPlayer
        if player_offset != -1:
            if player_offset < len(self.playersEligibleForAttack):
                player = self.playersEligibleForAttack[player_offset]
            else:
                return

        if len(player.deck) < amount:
            player.shuffle()

        cards = []
        for i in range(amount):
            cards.append(player.deck[i])
        self.buffer = cards
        return cards

    def get_top_trash_card(self):
        if len(self.trash) > 0:
            return self.trash[-1]
        else:
            return Card.Card("Null", 0, "Null")

    # player_offset - The player who has to discard cards. If it is not -1, it is an attack and uses the attack list
    # hand_check - Whether or not the hand size should be checked before proceeding
    def put_cards_play_area(self, player_offset, amount, hand_check=False):
        """Draw the specified amount of cards and move them to the play area
        check for negative numbers"""

        self.playerCompletedAction = False

        player = self.currentPlayer
        if player_offset != -1:
            if player_offset < len(self.playersEligibleForAttack):
                player = self.playersEligibleForAttack[player_offset]
            else:
                return

        if hand_check:
            if 7 < player.get_hand_size():
                return

        for i in range(amount):
            self.playerCompletedAction = False

            # If they aren't any cards left in the deck, shuffle the deck
            if len(player.deck) == 0:
                player.shuffle()

            # Make sure the deck hasn't been exhausted
            if len(player.deck) != 0:
                card = player.deck.pop(0)
                player.personalPlayArea.append(card)
                self.playerCompletedAction = True
            else:
                break

    # player_offset - The player who has to discard cards. If it is not -1, it is an attack and uses the attack list
    def move_cards(self, player_offset, loc1, loc2, cards, check_checked=False, check_answer=False):
        """Move cards from location 1 to location 2 if check is true and currentMoves isn't greater
        than maxmoves"""
        if check_checked:
            if check_answer:
                if self.check and self.playerAnswer:
                    return
            elif not self.check:
                return

        player = self.currentPlayer
        if player_offset != -1:
            if player_offset < len(self.playersEligibleForAttack):
                player = self.playersEligibleForAttack[player_offset]
            else:
                return

        if cards == "Buffer":
            cards = self.buffer
        elif cards == "Most Recent Played":  # The card is the most recently played one
            cards = player.personalPlayArea[-1]

        card_object_list = []
        # If only a single card is specified, make it into an array so the code treat it like an array
        if not isinstance(cards, list):
            cards = [cards]
        for card in cards:
            #
            if isinstance(card, Card.Card):
                card_object_list = cards
                break
            # Find the corresponding card object for all of the card names
            for aCard in allKingdomCards:
                if aCard.get_name() == card:
                    card_object_list.append(aCard)
                    break

        if loc1 == "Play Area":
            if loc2 == "Hand":
                for card in card_object_list:
                    if card in player.personalPlayArea:
                        player.personalPlayArea.remove(card)
                        player.hand.append(card)
        elif loc1 == "Hand":
            if loc2 == "Play Area":
                for card in card_object_list:
                    for h_card in player.hand:
                        if card.get_name() == h_card.get_name():
                            player.hand.remove(h_card)
                            player.personalPlayArea.append(h_card)
                            break
            elif loc2 == "Top of Deck":
                for card in card_object_list:
                    for h_card in player.hand:
                        if card.get_name() == h_card.get_name():
                            player.hand.remove(h_card)
                            player.deck.insert(0, h_card)
                            break

        self.currentMoves += 1

    def check_played_card(self, c_type, check_action=False):
        """Set checked to true if the most recent played card is the right type"""
        if check_action and not self.playerCompletedAction:
            return

        self.check = False
        if len(self.currentPlayer.personalPlayArea) >= 1:
            card = self.currentPlayer.personalPlayArea[-1]
            if card.c_type == c_type:
                self.check = True
                self.buffer = [card]

    # player_offset - The player who has to discard cards. If it is not -1, it is an attack and uses the attack list
    # location - The location of the cards to discard
    # check_answer - A toggle to prevent the discarding of cards if a condition isn't met
    def discard_cards(self, player_offset, location, check_answer=False):
        """Move the player's specified cards from the specified location to the their play area if the check is true"""

        cards = self.buffer  # The name of the cards to discard, may be a single card or an array

        self.playerCompletedAction = False

        if check_answer:
            if not self.playerAnswer:
                self.buffer = []
                return

        player = self.currentPlayer
        if player_offset != -1:
            if player_offset < len(self.playersEligibleForAttack):
                player = self.playersEligibleForAttack[player_offset]
            else:
                return

        self.playerCompletedAction, self.buffer = player.discard_card(cards, location)

    # player_offset - The player who has to trash cards. If it is not -1, it is an attack and uses the attack list
    # names - The name of the specific cards to trash. If it is "", then the names are in self.buffer
    # location - The location of the cards to trash
    # check_action - An internal check to prevent chained actions from happening
    #                   when the previous action in the chain doesn't
    def trash_cards(self, player_offset, names, location, check_action=False):
        """Add card(s) to the trash. Remove any trace of them from their previous location"""

        if check_action:
            if not self.playerCompletedAction:
                self.buffer = []
                return

        self.playerCompletedAction = False

        player = self.currentPlayer
        if player_offset != -1:
            if player_offset < len(self.playersEligibleForAttack):
                player = self.playersEligibleForAttack[player_offset]
            else:
                return

        if names == "":
            names = self.buffer

        self.playerCompletedAction, cards = player.trash_card(names, location)
        if self.playerCompletedAction:
            self.trash += cards

    def give_trashed_cards(self, check_answer=False):
        """Remove cards from the trash and give them to the specified player.
        """
        if check_answer and not self.playerAnswer:
            return

        card = self.trash.pop(0)
        self.currentPlayer.personalPlayArea.append(card)

    # player_offset - The player who is gaining cards. If it is not -1, it is an attack and uses the attack list
    # card - The name of the card that the player is gaining.
    # location - The location the cards are being added to such as the discard pile or the top of the deck.
    # check_last_action - Specifies whether or not this effect depends on the completion of the previous action
    def gain_cards(self, player_offset, card, location="Play Area", check_last_action=False):
        """Gain a card from the supply and place it in the play area unless specified otherwise. Decrease the supply
        pile by one and check to make sure a card is specified"""

        if check_last_action:
            if not self.playerCompletedAction:
                self.buffer = []
                return

        player = self.currentPlayer
        if player_offset != -1:
            if player_offset < len(self.playersEligibleForAttack):
                player = self.playersEligibleForAttack[player_offset]
            else:
                return

        if card == "":
            card = self.buffer

        if isinstance(card, list):
            card = card[0]

        for s_card in self.supplyCards.keys():
            # If the card exists in the supply, proceed
            if s_card.get_name() == card:
                # If the supply is not empty, proceed
                if self.supplyCards[s_card] > 0:
                    # Remove a card from the supply and add it to the player's play area
                    self.supplyCards[s_card] -= 1
                    return player.gain_card(s_card, location)
                else:
                    return False
        return False

    # player_offset - The player who has to select the cards. If it is not -1, it is an attack and uses the attack list
    # location - The location from which the player is selecting the card(s).
    # constraints - The constraints on the cards that the player can select. These can be type, number of, and cost.
    # check_last_action - Specifies whether or not this effect depends on the completion of the previous action
    def select_cards(self, player_offset, location, constraints, check_last_action=False):
        """Figure out the location from which the cards are being selected from
        Filter the cards according to the constraints
        If player is an array, check to see if the array is long enough for the player to exist
        Set the buffer to the selectable cards and set the inputNeededFlag"""

        if check_last_action:
            if not self.playerCompletedAction:
                self.buffer = []
                return

        self.playerCompletedAction = False

        player = self.currentPlayer
        if player_offset != -1:
            if player_offset < len(self.playersEligibleForAttack):
                player = self.playersEligibleForAttack[player_offset]
            else:
                return

        cards = ["Select"]
        selectable_cards = []

        # Set this so that the main program knows when input is needed
        self.inputNeededFlag = True

        # Set the location from where the cards are being selected
        if location == "Hand":
            selectable_cards = player.hand.copy()
        elif location == "Play Area":
            selectable_cards = player.personalPlayArea.copy()
        elif location == "Supply":
            selectable_cards = list(self.supplyCards.keys())
        elif location == "0 Play Area":
            if len(self.playersEligibleForAttack) < 1:
                return
            selectable_cards = self.playersEligibleForAttack[0].personalPlayArea.copy()
        elif location == "1 Play Area":
            if len(self.playersEligibleForAttack) < 2:
                return
            selectable_cards = self.playersEligibleForAttack[1].personalPlayArea.copy()
        elif location == "2 Play Area":
            if len(self.playersEligibleForAttack) < 3:
                return
            selectable_cards = self.playersEligibleForAttack[2].personalPlayArea.copy()

        # Filter the cards according to type constraints
        if "Victory" in constraints:
            # Remove any card that is not a Victory card
            for card in reversed(selectable_cards):
                if not isinstance(card, Card.VictoryCard):
                    selectable_cards.remove(card)
        elif "Action" in constraints:
            # Remove any card that is not an Action card
            for card in reversed(selectable_cards):
                if not isinstance(card, Card.ActionCard):
                    selectable_cards.remove(card)
        elif "Treasure" in constraints:
            # Remove any card that is not a Treasure card
            for card in reversed(selectable_cards):
                if not isinstance(card, Card.TreasureCard):
                    selectable_cards.remove(card)

        # Filter the cards according to cost constraints
        if "$" in constraints:
            i = constraints.find("$")
            cost = constraints[i+3:i+4]  # Just the number/cost that it has to be less than

            if cost == "T":  # The cost is dependent on the top card of the trash pile
                t_card = self.get_top_trash_card()
                if t_card.get_name() == "Null":
                    self.buffer = []
                    return
                else:
                    # Add the cost of the trashed card and the boost together
                    cost = t_card.get_cost() + int(constraints[i+5:i+6])
            else:  # The cost is a numerical value
                cost = int(cost)

            # Remove cards that cost more than the specified amount
            for card in reversed(selectable_cards):
                if card.get_cost() > cost:
                    selectable_cards.remove(card)

        if len(selectable_cards) == 0:
            self.inputNeededFlag = False
            return

        cards.append(selectable_cards)

        # Add card amount constraints to the array that will be passed to the buffer so that the cards can be filtered
        i = constraints.find("#")
        num_constraints = constraints[i:i + 4]  # Find the constraints on the number of cards
        cards.append(num_constraints)

        self.buffer = cards
        self.playerCompletedAction = True

    # check - Whether or not to check the playeranswer field
    def shuffle_deck(self, check=True):
        """Shuffle the specified player's deck."""
        if check:
            if self.playerAnswer:
                self.currentPlayer.shuffle()

    # amount - The amount of actions to add
    def add_actions(self, amount):
        """Add the specified amount of actions to the current player"""
        self.currentPlayer.add_actions(amount)

    # amount - The amount of buys to add
    def add_buys(self, amount):
        """Add the specified amount of buys to the current player"""
        self.currentPlayer.add_buys(amount)

    # amount - The amount of coins to add
    # check_last_action - If the effect depends on the completion of the previous action
    def add_coins(self, amount, check_last_action=False):
        """Add the specified amount of coins to the current player"""
        if check_last_action:
            if not self.playerCompletedAction:
                return

        self.currentPlayer.add_coins(amount)

    # question - The question to ask the user
    # check_last - Toggle to check if a function completed ("Action") or a certain result of a function ("Function")
    def ask_player(self, question, check_last="", player_offset=-1):
        """Ask the current player a question
         Their answer should be set to self.playerAnswer"""

        if player_offset != -1:
            if player_offset >= len(self.playersEligibleForAttack):
                self.playerAnswer = False
                return

        if check_last == "Action":
            if not self.playerCompletedAction:
                self.playerAnswer = False
                return
        elif check_last == "Function":
            if not self.check:
                self.playerAnswer = False
                return

        if len(self.buffer) > 0:
            if isinstance(self.buffer[0], Card.Card):
                question += " (" + self.buffer[0].get_name() + ")"

        self.inputNeededFlag = True
        self.buffer = ["Question", question]

    def end_turn(self):
        """Reset all variables
        Move the cards in the play area to the discard pile"""
        self.buffer = [""]
        self.playerAnswer = False
        self.playerCompletedAction = False
        self.check = False
        self.playersEligibleForAttack = []
        self.currentMoves = 0
        self.inputNeededFlag = False

        # Clean up the current player area and set them up for the next turn
        self.currentPlayer.end_turn()

        for player in self.players:
            if len(player.personalPlayArea) > 0:
                player.clean_up_play_area()

        # Switch the current player to the next player in the array
        self.currentPlayer = self.players[(self.players.index(self.currentPlayer) + 1) % len(self.players)]

    def check_game_end(self):
        if self.supplyCards[allKingdomCards[31]] == 0:
            return True
        empty_piles = 0
        for cardsLeft in self.supplyCards:
            if cardsLeft == 0:
                empty_piles += 1

        if empty_piles >= 3:
            return True

        return False

    def poll_players_for_attack(self):
        """query self.players - self.currentPlayer
        set buffer to a list of players that have a moat"""
        potential_players = []
        for player in self.players:
            if player != self.currentPlayer:
                potential_players.append(player)

        for player in reversed(potential_players):
            if self.allKingdomActionCards["Moat"] in player.hand:
                potential_players.remove(player)
        self.playersEligibleForAttack = potential_players

    def get_player_objects(self):
        """Translate the player's names that are in the buffer to their corresponding player object"""
        matches = []
        for given_name in range(len(self.buffer)):
            for player in range(len(self.players)):
                if self.players[player].get_name() == given_name:
                    matches.append(self.players[player])
        return matches

    def print_game_state(self):
        print("*******Current Game State*******")
        for card in self.supplyCards:
            print(card.name + " : " + str(self.supplyCards[card]) + ", ", end='')
        print()
        for player in self.players:
            print(player)
        print()
        print("Trash: ", end='')
        for card in self.trash:
            print(card, end='')
        print()
        for card in self.playArea:
            print(card, end='')
        print()
        print("Process Queue: ", end='')
        print(self.processQueue)
        print(self.currentPlayer.name)
        print("********************************")
        print()
