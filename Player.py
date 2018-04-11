import Card
import random


class Player:
    def __init__(self, name):
        self.name = name

        # Set up the player's deck
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
        """Create a string that contains every attribute of the Player instance"""
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

    # amount - The number of cards to draw
    def draw_card(self, amount):
        """Move cards from the beginning of the deck and add it to the hand."""

        added_cards = []

        for i in range(amount):
            # The top of the deck will be the beginning of the list
            # If the deck is empty, shuffle the discard to make it the deck
            if len(self.deck) == 0 and len(self.discard) != 0:
                self.shuffle()

            # Check to make sure the deck has not been exhausted for this turn
            if len(self.deck) != 0:
                card = self.deck.pop(0)
                self.hand.append(card)
                added_cards.append(card)

        return added_cards

    # names - The names of the cards to remove
    # location - The location of the cards to remove
    def trash_card(self, names, location):
        """Remove cards from the specified location.
        Return if the operation succeeded and the cards that were removed."""

        completed = False
        removed_cards = []  # Keeps track of removed cards so they can be added to the trash

        if not isinstance(names, list):
            names = [names]

        for card_name in names:
            completed = False  # If there are multiple cards, this field resets in case one fails
            if location == "Hand":
                for card in self.hand:
                    if card.get_name() == card_name:
                        self.hand.remove(card)
                        removed_cards.append(card)
                        completed = True
            elif location == "Play Area":
                for card in self.personalPlayArea:
                    if card.get_name() == card_name:
                        self.personalPlayArea.remove(card)
                        completed = True

        if completed:
            return True, removed_cards
        else:
            # Add the removed cards back to their location so it can be retried
            if location == "Hand":
                self.hand += removed_cards
            elif location == "Play Area":
                self.personalPlayArea += removed_cards
            return False, []

    # names - The names of the cards to discard
    # location - The location of the cards to discard
    def discard_card(self, names, location):
        """Move cards from the specified location to the play area."""

        completed = False
        discarded_cards = []

        if not isinstance(names, list):
            names = [names]

        if location == "Hand":
            for card in names:
                completed = False
                for hand_card in self.hand:
                    if card == hand_card.get_name():
                        self.hand.remove(hand_card)
                        self.personalPlayArea.append(hand_card)
                        discarded_cards.append(hand_card)
                        completed = True
                        break  # Move on to the next card name
        elif location == "Top of Deck":
            card = self.deck.pop(0)
            self.personalPlayArea.append(card)
            discarded_cards.append(card)
            completed = True

        return completed, discarded_cards

    # card - The card object that the player is gaining
    # location - The location the card will be added to
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

    # amount - The number of actions to add
    def add_actions(self, amount):
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
        """Return the names of all Action cards in the player's hand."""
        action_cards = []
        for card in self.hand:
            if "Action" in card.c_type:
                action_cards.append(card.get_name())
        return action_cards

    def get_current_buys(self):
        """Return the total amount of buys that the player has including card effects."""
        return self.buys

    def end_turn(self):
        self.discard += self.hand  # Discard the hand
        self.discard += self.personalPlayArea  # Discard any cards that were used or gained this turn
        self.hand = []
        self.personalPlayArea = []

        self.actions = 1
        self.coins = 0
        self.buys = 1

        self.draw_card(5)

    def clean_up_play_area(self):
        self.discard += self.personalPlayArea # Discard any cards that were used or gained this turn
        self.personalPlayArea = []
