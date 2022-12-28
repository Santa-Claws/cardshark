import random
from typing import List
from card import Card


class Deck:
    suits = {'clubs': '♣', 'diamonds': '♦', 'spades': '♠', 'hearts': '♥'}
    names = [(str(n), n) for n in range(2, 11)] + [('J', 11), ('Q', 12), ('K', 13), ('A', 14)]

    def __init__(self, size=52):
        self.size = size
        cardz_raw = zip(Deck.names * len(Deck.suits), list(Deck.suits.values()) * len(Deck.names))
        self.cards = [Card(name, suit, value) for (name, value), suit in cardz_raw]
        random.shuffle(self.cards)

    def print(self):
        for i in range(0, len(self.cards), 13):
            [print(f"{str(card)}, ", end="") for card in self.cards[i:i + 13]]
            print()

    def deal(self, num_players, num_cards) -> List[List[Card]]:
        if num_players * num_cards > self.size:
            raise RuntimeError("not enough cards!")
        # its a few lines of code
        player_hands = [[] for _ in range(num_players)]
        for n in range(num_cards):
            for i in range(num_players):
                player_hands[i].append(self.cards.pop(0))
        return player_hands

    @staticmethod
    def show_deck(deck):
        print(deck)

