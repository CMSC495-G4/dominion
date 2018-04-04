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

    def gain_card(self, name, location="Personal Play Area"):
        """Add the given card to the player's area.
        Does not handle removing a card from the supply only the actions that happen to the player"""

        card = Game.allKingdomCards[name]
        if location == "Personal Play Area":
            self.personalPlayArea.append(card)
        elif location == "Hand":
            self.hand.append(card)
        elif location == "Top of Deck":
            self.deck.insert(0, card)

    def shuffle(self):
        """Take the cards in the discard pile, add them to the deck, shuffle them, and make them the new deck.
        Clear the discard pile."""

        self.deck += self.discard
        random.shuffle(self.deck)
        self.discard = []

    def add_actions(self, amount):
        """"""

    def get_name(self):
        return self.name

    def get_hand_size(self):
        return len(self.hand)

    def get_current_gold(self):
        """"""

    def get_current_actions(self):
        """"""

    def get_current_buys(self):
        """"""
