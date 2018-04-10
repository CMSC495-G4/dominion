import Card
import random
import Game


class Player:
    def __init__(self, name):
        self.name = name

        self.deck = []
        for i in range(7):
            self.deck.append(Card.TreasureCard("Copper", 0, "Treasure", 1))
        for i in range(3):
            self.deck.append(Card.VictoryCard("Estate", 2, "Victory", 1))

        self.discard = []
        self.hand = []
        self.personalPlayArea = []
        self.shuffle()
        self.draw_card(5)

        self.actions = 1
        self.coins = 0
        self.buys = 1

    def __str__(self):
        string = self.name + "\n\tHand: "
        for card in self.hand:
            string += str(card) + " "
        string += "\n\tDeck: "
        for card in self.deck:
            string += str(card) + " "
        string += "\n\tDiscard: "
        for card in self.discard:
            string += str(card) + " "
        string += "\n\tPlay Area: "
        for card in self.personalPlayArea:
            string += str(card) + " "
        string += "\n\tActions: " + str(self.actions)
        string += "\n\tCoins: " + str(self.coins)
        string += "\n\tBuys: " + str(self.buys)
        return string

    def draw_card(self, amount):
        """Draw a specified amount of cards from the top of the deck and add it to the hand"""

        addedCards = []

        for i in range(amount):
            # The top of the deck will be the beginning of the list
            # If the deck is empty, shuffle the discard to make it the deck
            if len(self.deck) == 0 and len(self.discard) != 0:
                self.shuffle()

            # Check to make sure the deck has not been exhausted for this turn
            if len(self.deck) != 0:
                card = self.deck.pop(0)
                self.hand.append(card)
                addedCards.append(card)

        return addedCards

    def trash_card(self, name):
        """"""

    def discard_card(self, name):
        """Discard to the play area"""

    def gain_card(self, card, location="Personal Play Area"):
        """Add the given card to the player's area.
        Does not handle removing a card from the supply only the actions that happen to the player"""

        if location == "Play Area":
            self.personalPlayArea.append(card)
            return True
        elif location == "Hand":
            self.hand.append(card)
            return True
        elif location == "Top of Deck":
            self.deck.insert(0, card)
            return True
        return False

    def shuffle(self):
        """Take the cards in the discard pile, add them to the deck, shuffle them, and make them the new deck.
        Clear the discard pile."""

        self.deck += self.discard
        random.shuffle(self.deck)
        self.discard = []

    def add_actions(self, amount):
        """"""
        self.actions += amount

    def get_name(self):
        return self.name

    def get_hand_size(self):
        return len(self.hand)

    def get_current_coins(self):
        """Return the total amount of coins that the player has including their hand and card effects."""
        for card in self.hand:
            if "Treasure" in card.c_type:
                self.coins += card.get_coins()
        return self.coins

    def get_current_actions(self):
        return self.actions

    def has_action_cards(self):
        for card in self.hand:
            if "Action" in card.c_type:
                return True
        return False

    def get_action_cards(self):
        action_cards = []
        for card in self.hand:
            if "Action" in card.c_type:
                action_cards.append(card.get_name())
        return action_cards

    def get_current_buys(self):
        """Return the total amount of buys that the player has including card effects."""
        return self.buys

    def end_turn(self):
        self.discard += self.hand
        self.discard += self.personalPlayArea
        self.hand = []
        self.personalPlayArea = []

        self.actions = 1
        self.coins = 0
        self.buys = 1

        self.draw_card(5)
