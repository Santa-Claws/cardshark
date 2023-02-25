from typing import List

from card import Card


class Player:
    def __init__(self, name, cards: List[Card], socket=None, cash=1000, ai=False):
        self.name = name
        self.cards = cards
        self.socket = socket
        self.cash = cash
        self.ai = ai

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


