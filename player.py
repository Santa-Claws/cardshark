import json
from typing import List

from card import Card


class Player:
    def __init__(self, name, cards: List[Card], message=None, cash=1000, ai=False):
        self.name = name
        self.cards = cards
        self.message = message
        self.cash = cash
        self.ai = ai

    def __str__(self):
        return json.dumps({
            'name': self.name,
            'message': str(self.message)
        })

    def __repr__(self):
        return self.__str__()
