class Card:
    def __init__(self, name, cost, ctype):
        self.name = name
        self.cost = cost
        self.ctype = ctype

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_cost(self):
        return self.cost


class VictoryCard(Card):
    def __init__(self, name, cost, ctype, points):
        Card.__init__(self, name, cost, ctype)
        self.points = points


class TreasureCard(Card):
    def __init__(self, name, cost, ctype, coins):
        Card.__init__(self, name, cost, ctype)
        self.coins = coins

    def get_coins(self):
        return self.coins


class ActionCard(Card):
    def __init__(self, name, cost, ctype, action):
        Card.__init__(self, name, cost, ctype)
        self.action = action


class ReactionCard(ActionCard):
    def __init__(self, name, cost, ctype, action, trigger):
        ActionCard.__init__(self, name, cost, ctype, action)
        self.trigger = trigger
