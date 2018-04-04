import Player
import Card
import random
import time

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
                   Card.TreasureCard("Copper", 1, "Treasure", 0),
                   Card.TreasureCard("Silver", 2, "Treasure", 3),
                   Card.TreasureCard("Gold", 3, "Treasure", 6),
                   Card.VictoryCard("Curse", 0, "Victory", -1),
                   Card.VictoryCard("Estate", 2, "Victory", 1),
                   Card.VictoryCard("Duchy", 5, "Victory", 3),
                   Card.VictoryCard("Province", 8, "Victory", 6)]


def diff_of_list(lst1, lst2):
    """Return a list with all occurrences of elements of lst2 removed from lst1"""

    return [item for item in lst1 if item not in lst2]


class Game:
    def __init__(self, players):
        self.supplyCards = {}
        self.players = players
        self.trash = []
        self.playArea = []
        self.processQueue = []
        self.currentPlayer = random.choice(players)

        # FIX THESE SO THE NAMES AREN'T AS CONFUSING
        self.buffer = [""]
        self.playerAnswer = False
        self.playerCompletedAction = False
        self.check = False
        self.playersEligibleForAttack = []
        self.currentMoves = 0
        self.inputNeededFlag = False

        self.allKingdomActionCards = {
            "Cellar": [[self.add_actions, self.currentPlayer, 1],
                       [self.select_cards, self.currentPlayer, "Hand"],
                       [self.discard_cards, self.currentPlayer, self.buffer, "Hand"],
                       [self.draw_cards, self.currentPlayer, self.buffer]],

            "Chapel": [[self.select_cards, self.currentPlayer, "Hand", "#<=4"],
                       [self.trash_cards, self.currentPlayer, self.buffer, "Hand"]],

            "Moat": [[self.draw_cards, self.currentPlayer, 2]],

            "Chancellor": [[self.add_coins, self.currentPlayer, 2],
                           [self.ask_player, self.currentPlayer, "Do you want to shuffle your deck?"],
                           [self.shuffle_deck, self.currentPlayer, self.playerAnswer]],

            "Village": [[self.draw_cards, self.currentPlayer, 1], [self.add_actions, self.currentPlayer, 2]],

            "Woodcutter": [[self.add_buys, self.currentPlayer, 1], [self.add_coins, self.currentPlayer, 2]],

            "Workshop": [[self.select_cards, self.currentPlayer, "Supply", "#==1 $<=4"],
                         [self.gain_cards, self.currentPlayer, self.buffer]],

            "Bureaucrat": [[self.gain_cards, self.currentPlayer, "Silver", "top of deck"],
                           [self.poll_players_for_attack],
                           [self.select_cards, [self.playersEligibleForAttack, 0], "Hand", "#==1 Victory"],
                           [self.move_cards, [self.playersEligibleForAttack, 0], "Hand", "Top of Deck", self.buffer],
                           [self.select_cards, [self.playersEligibleForAttack, 1], "Hand", "#==1 Victory"],
                           [self.move_cards, [self.playersEligibleForAttack, 1], "Hand", "Top of Deck", self.buffer],
                           [self.select_cards, [self.playersEligibleForAttack, 2], "Hand", "#==1 Victory"],
                           [self.move_cards, [self.playersEligibleForAttack, 2], "Hand", "Top of Deck", self.buffer]],

            "Feast": [[self.trash_cards, self.currentPlayer, "Feast", "Play Area"],
                      [self.select_cards, self.currentPlayer, "Supply", "#==1 $>=5"],
                      [self.gain_cards, self.currentPlayer, self.buffer]],

            "Militia": [[self.add_coins, self.currentPlayer, 2], [self.poll_players_for_attack],
                        [self.select_cards, [self.playersEligibleForAttack, 0], "Hand", "#==2"],
                        [self.discard_cards, [self.playersEligibleForAttack, 0], self.buffer, "Hand"],
                        [self.select_cards, [self.playersEligibleForAttack, 1], "Hand", "#==2"],
                        [self.discard_cards, [self.playersEligibleForAttack, 1], self.buffer, "Hand"],
                        [self.select_cards, [self.playersEligibleForAttack, 2], "Hand", "#==2"],
                        [self.discard_cards, [self.playersEligibleForAttack, 2], self.buffer], "Hand"],

            "Moneylender": [[self.trash_cards, self.currentPlayer, "Copper", "Hand"],
                            [self.add_coins, self.currentPlayer, 3, self.playerCompletedAction]],

            "Remodel": [[self.select_cards, self.currentPlayer, "Hand"],
                        [self.trash_cards, self.currentPlayer, self.buffer, "Hand"],
                        [self.select_cards, self.currentPlayer, "Supply", "#==1 $<=2+" + str(self.get_top_trash_card().get_cost())],
                        [self.gain_cards, self.currentPlayer, self.buffer]],

            "Smithy": [[self.draw_cards, self.currentPlayer, 3]],

            "Spy": [[self.draw_cards, self.currentPlayer, 1], [self.add_actions, self.currentPlayer, 1],
                    [self.poll_players_for_attack], [self.reveal_top_cards, self.currentPlayer, 1],
                    [self.ask_player, self.currentPlayer, "Yes/No"],
                    [self.discard_cards, self.currentPlayer, self.buffer, "Top of Deck", self.playerAnswer],
                    [self.reveal_top_cards, [self.playersEligibleForAttack, 0], 1],
                    [self.ask_player, self.currentPlayer, "Yes/No"],
                    [self.discard_cards, [self.playersEligibleForAttack, 0], self.buffer, "Top of Deck",
                     self.playerAnswer], [self.reveal_top_cards, [self.playersEligibleForAttack, 1], 1],
                    [self.ask_player, self.currentPlayer, "Yes/No"],
                    [self.discard_cards, [self.playersEligibleForAttack, 1], self.buffer, "Top of Deck",
                     self.playerAnswer], [self.reveal_top_cards, [self.playersEligibleForAttack, 2], 1],
                    [self.ask_player, self.currentPlayer, "Yes/No"],
                    [self.discard_cards, [self.playersEligibleForAttack, 2], self.buffer, "Top of Deck",
                     self.playerAnswer]],

            "Thief": [[self.poll_players_for_attack], [self.put_cards_play_area, [self.playersEligibleForAttack, 0], 2],
                      [self.select_cards, self.currentPlayer, "Play Area", "#<=1 Treasure"],
                      [self.trash_cards, [self.playersEligibleForAttack, 0], self.buffer, "Play Area",
                       self.playerCompletedAction],
                      [self.ask_player, self.currentPlayer, "Yes/No", self.playerCompletedAction],
                      [self.give_trashed_cards, self.currentPlayer, self.buffer, self.playerAnswer],
                      [self.put_cards_play_area, [self.playersEligibleForAttack, 1], 2],
                      [self.select_cards, self.currentPlayer, "Play Area", "#<=1 Treasure"],
                      [self.trash_cards, [self.playersEligibleForAttack, 1], self.buffer, "Play Area",
                       self.playerCompletedAction],
                      [self.ask_player, self.currentPlayer, "Yes/No", self.playerCompletedAction],
                      [self.give_trashed_cards, self.currentPlayer, self.buffer, self.playerAnswer],
                      [self.put_cards_play_area, [self.playersEligibleForAttack, 2], 2],
                      [self.select_cards, self.currentPlayer, "Play Area", "#<=1 Treasure"],
                      [self.trash_cards, [self.playersEligibleForAttack, 2], self.buffer, "Play Area",
                       self.playerCompletedAction],
                      [self.ask_player, self.currentPlayer, "Yes/No", self.playerCompletedAction],
                      [self.give_trashed_cards, self.currentPlayer, self.buffer, self.playerAnswer]],

            "Throne Room": [[self.select_cards, self.currentPlayer, "Hand", "Action"],
                            [self.add_card_blocks, self.currentPlayer, self.buffer],
                            [self.add_card_blocks, self.currentPlayer, self.buffer]],

            "Council Room": [[self.draw_cards, [diff_of_list(self.players, [self.currentPlayer]), 0], 4],
                             [self.draw_cards, [diff_of_list(self.players, [self.currentPlayer]), 1], 1],
                             [self.draw_cards, [diff_of_list(self.players, [self.currentPlayer]), 2], 1],
                             [self.draw_cards, self.currentPlayer, 4]],

            "Festival": [[self.add_actions, self.currentPlayer, 2], [self.add_buys, self.currentPlayer, 1],
                         [self.add_coins, self.currentPlayer, 2]],

            "Laboratory": [[self.draw_cards, self.currentPlayer, 2], [self.add_actions, self.currentPlayer, 1]],

            # The check is testing to see if the card is an action card, if it is, self.check is true
            # The player is being asked if they want to set aside the Action card, if they do, self.playerAnswer is true
            # Therefore, move the card to the hand if they say not to set it aside or if the card is not an action
            "Library": [[self.put_cards_play_area, self.currentPlayer, 7 - self.currentPlayer.get_hand_size()],
                        [self.check_played_card, self.currentPlayer, "Action"],
                        [self.ask_player, self.currentPlayer, "Yes/No", self.check],
                        [self.move_cards, self.currentPlayer, "Play Area", "Hand", self.buffer, # CHANGE BUFFER TO MOST RECENT PLAYED CARD
                         not self.playerAnswer or not self.check],
                        [self.add_card_blocks, "Library", 7 > self.currentPlayer.get_hand_size()]],

            "Market": [[self.draw_cards, self.currentPlayer, 1], [self.add_actions, self.currentPlayer, 1],
                       [self.add_buys, self.currentPlayer, 1], [self.add_coins, self.currentPlayer, 1]],

            "Mine": [[self.select_cards, self.currentPlayer, "Hand", "#==1 Treasure"],
                     [self.trash_cards, self.currentPlayer, self.buffer, "Hand"],
                     [self.select_cards, self.currentPlayer, "Supply",
                      "#==1 $<=3+" + str(self.get_top_trash_card().get_cost()) + " Treasure"],
                     [self.gain_cards, self.currentPlayer, self.buffer]],

            "Witch": [[self.draw_cards, self.currentPlayer, 2],
                      [self.gain_cards, [diff_of_list(self.players, [self.currentPlayer]), 0], "Curse"],
                      [self.gain_cards, [diff_of_list(self.players, [self.currentPlayer]), 1], "Curse"],
                      [self.gain_cards, [diff_of_list(self.players, [self.currentPlayer]), 2], "Curse"]],

            "Adventurer": [[self.put_cards_play_area, self.currentPlayer, 1],
                           [self.check_played_card, self.currentPlayer, "Treasure"],
                           [self.move_cards, self.currentPlayer, "Play Area", "Hand", [self.playArea, -1], self.check, 2],
                           [self.add_card_blocks, "Adventurer", 2 < self.currentMoves]]
        }

    def get_supply_cards(self):
        return self.supplyCards

    def get_top_trash_card(self):
        if len(self.trash) > 0:
            return self.trash[-1]
        else:
            return Card.Card("Null", 0, "Null")

    def select_kingdom_cards(self):
        """Randomly generate 10 numbers to select 10 Kingdom cards
        Add those cards to the supply with the appropriate amount
        Add the Treasure and Victory cards to the supply"""

        chosen = []
        for i in range(10):
            randCard = random.randint(0, 24)
            if randCard not in chosen:
                self.supplyCards[allKingdomCards[randCard]] = 10  # Add all Kingdom cards to supply
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
        numOfActions = self.add_card_blocks(name)
        self.move_cards(self.currentPlayer, "Hand", "Play Area", name)
        return numOfActions

    def add_card_blocks(self, name):
        """Query database for list of actions
        Split actions into individual actions
        Add each action with the appropriate arguments to the queue
        Return the amount of actions found"""
        actions = self.allKingdomActionCards[name]
        for action in actions:
            self.processQueue.append(action)
        return len(actions)

    def draw_cards(self, player, amount):
        """Draw cards from the specified player's deck and add them to their hand
        Return the specific cards drawn"""
        return player.draw_card(amount)

    def reveal_top_cards(self, player, amount):
        """If player object is an array, check to see if the array is long enough for the player to exist
        Set the buffer to the card objects so that discard_cards can find the names
        Return the card object (CHANGE IF NEEDED, DOES NOT AFFECT INTERNAL FUNCTIONS)
        Revealed cards are NOT moved, the card object is merely returned"""
        if isinstance(player, list):
            if len(player[0]) > player[1]:
                player = player[0][player[1]]
            else:
                return []
        cards = []
        for i in range(amount):
            cards.append(player.deck[i])
        self.buffer = cards
        return cards

    def put_cards_play_area(self, player, amount):
        """Draw the specified amount of cards and move them to the play area
        check for negative numbers"""
        # This function accepts an array of players and an index to specify one player so check to make sure that
        #   player exists
        if isinstance(player, list):
            if len(player[0]) > player[1]:
                player = player[0][player[1]]
            else:
                return []

        cards = []
        for i in range(amount):
            # If they aren't any cards left in the deck, shuffle the deck
            if len(player.deck) == 0:
                player.shuffle()

            # Make sure the deck hasn't been exhausted
            if len(player.deck) != 0:
                card = player.deck.pop()
                cards.append(card)
                player.personalPlayArea.append(card)
            else:
                break

        return cards

    def move_cards(self, player, loc1, loc2, cards, check=True, maxmoves=100):
        """Move cards from location 1 to location 2 if check is true and currentMoves isn't greater
        than maxmoves"""
        if check and maxmoves > self.currentMoves:
            if loc1 == "Play Area":
                if loc2 == "Hand":
                    for card in cards:
                        player.personalPlayArea.remove(card)
                        player.hand.append(card)
                else:
                    return False
            elif loc1 == "Hand":
                if loc2 == "Play Area":
                    for card in cards:
                        player.hand.remove(card)
                        player.personalPlayArea.append(card)
                if loc2 == "Top of Deck":
                    for card in cards:
                        player.hand.remove(card)
                        player.deck.insert(0, card)
            else:
                return False

    def check_played_card(self, player, ctype):
        """Set checked to true if the most recent played card is the right type"""
        if len(player.personalPlayArea) >= 1:
            card = player.personalPlayArea[-1]
            if card.ctype == ctype:
                return True

        return False

    def discard_cards(self, player, cards, location, check=True):
        """If player is an array, check to see if the array is long enough for the player to exist
        Discard the player's specified cards from the specified location if the check is true
        The specified cards are the name's only not the actual object"""
        if check:
            # This function accepts an array of players and an index to specify one player so check to make sure that
            #   player exists
            if isinstance(player, list):
                if len(player[0]) > player[1]:
                    player = player[0][player[1]]
                else:
                    return []

            if location == "Hand":
                for card in cards:
                    for handCard in player.hand:
                        if card == handCard.get_name():
                            player.hand.remove(handCard)
                            player.personalPlayArea.append(handCard)
                            break
            elif location == "Top of Deck":
                card = player.deck.pop(0)
                player.personalPlayArea.append(card)

    def trash_cards(self, player, names, location, check=True):
        """Add card(s) to the trash. Remove any trace of them from their previous location"""
        self.playerCompletedAction = False

        if check:
            # This function accepts an array of players and an index to specify one player so check to make sure that
            #   player exists
            if isinstance(player, list):
                if len(player[0]) > player[1]:
                    player = player[0][player[1]]
                else:
                    return []
            if isinstance(names, list):
                for cardname in names:
                    if location == "Hand":
                        for card in player.hand:
                            if card.get_name() == cardname:
                                player.hand.remove(card)
                                self.trash.append(card)
                                self.playerCompletedAction = True
                    elif location == "Play Area":
                        for card in player.personalPlayArea:
                            if card.get_name() == cardname:
                                player.personalPlayArea.remove(card)
                                self.trash.append(card)
                                self.playerCompletedAction = True
            else:
                if location == "Hand":
                    for card in player.hand:
                        if card.get_name() == names:
                            player.hand.remove(card)
                            self.trash.append(card)
                            self.playerCompletedAction = True
                elif location == "Play Area":
                    for card in player.personalPlayArea:
                        if card.get_name() == names:
                            player.personalPlayArea.remove(card)
                            self.trash.append(card)
                            self.playerCompletedAction = True

    def give_trashed_cards(self, player, cards, check=True):
        """Remove cards from the trash and give them to the specified player.
        """
        if check:
            if isinstance(cards, list):
                for card in cards:
                    for tcard in self.trash:
                        if tcard.get_name() == card:
                            self.trash.remove(tcard)
                            player.personalPlayArea.append(tcard)
            else:
                for tcard in self.trash:
                    if tcard.get_name() == cards:
                        self.trash.remove(tcard)
                        player.personalPlayArea.append(tcard)

    # card is the name of the card that the player is gaining
    # location is the location the cards are being added to such as the discard pile or the top of the deck
    def gain_cards(self, player, card, location="Play Area"):
        """Gain a card from the supply and place it in the play area unless specified otherwise. Decrease the supply
        pile by one and check to make sure a card is specified"""
        for scard in self.supplyCards.keys():
            if scard.get_name() == card:
                self.supplyCards[scard] -= 1
                if location == "Play Area":
                    player.personalPlayArea.append(scard)
                elif location == "Top of Deck":
                    player.deck.insert(0, scard)
                break

    def select_cards(self, player, location, constraints):
        """If player is an array, check to see if the array is long enough for the player to exist"""
        self.buffer = [location, constraints]
        # This function accepts an array of players and an index to specify one player so check to make sure that
        #   player exists
        if isinstance(player, list):
            if len(player[0]) > player[1]:
                player = player[0][player[1]]
            else:
                return []

        self.inputNeededFlag = True
        while self.buffer != [location, constraints]:
            time.sleep(5)
        self.inputNeededFlag = False

    def shuffle_deck(self, player, check=True):
        """Shuffle the specified player's deck."""
        if check:
            player.shuffle()

    def add_actions(self, player, amount):
        """Add the specified amount of actions to the specified player"""
        player.add_actions(amount)

    def add_buys(self, player, amount):
        """Add the specified amount of buys to the specified player"""
        player.add_buys(amount)

    def add_coins(self, player, amount):
        """Add the specified amount of coins to the specified player"""
        player.add_coins(amount)

    def ask_player(self, player, question, check):
        """Ask the player a yes or no question and set their answer to self.playerAnswer"""
        if check:
            self.playerAnswer = [player, question]
            self.inputNeededFlag = True
            while self.playerAnswer != [player, question]:
                time.sleep(5)
            self.inputNeededFlag = False

    def poll_players_for_attack(self):
        """query self.players - self.currentPlayer
        set buffer to a list of players that have a moat"""
        potentialPlayers = diff_of_list(self.players, self.currentPlayer)
        for player in potentialPlayers:
            if self.allKingdomActionCards["Moat"] in player.hand:
                potentialPlayers.remove(player)
        self.playersEligibleForAttack = potentialPlayers

    def get_player_objects(self):
        """Translate the player's names that are in the buffer to their corresponding player object"""
        matches = []
        for givenname in range(len(self.buffer)):
            for player in range(len(self.players)):
                if self.players[player].get_name() == givenname:
                    matches.append(self.players[player])
        return matches

    def print_game_state(self):
        for card in self.supplyCards:
            print(card.name + " : " + str(self.supplyCards[card]) + ", ", end='')
        print()
        for player in self.players:
            print(player)
        print()
        for card in self.trash:
            print(card, end='')
        print()
        for card in self.playArea:
            print(card, end='')
        print()
        print(self.processQueue)
        print(self.currentPlayer.name)