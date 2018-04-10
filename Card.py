class Card:
    def __init__(self, name, cost, c_type):
        self.name = name
        self.cost = cost
        self.c_type = c_type

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_cost(self):
        return self.cost


class VictoryCard(Card):
    def __init__(self, name, cost, c_type, points):
        Card.__init__(self, name, cost, c_type)
        self.points = points


class TreasureCard(Card):
    def __init__(self, name, cost, c_type, coins):
        Card.__init__(self, name, cost, c_type)
        self.coins = coins

    def get_coins(self):
        return self.coins


class ActionCard(Card):
    def __init__(self, name, cost, c_type, action):
        Card.__init__(self, name, cost, c_type)
        self.action = action


class ReactionCard(ActionCard):
    def __init__(self, name, cost, c_type, action, trigger):
        ActionCard.__init__(self, name, cost, c_type, action)
        self.trigger = trigger
