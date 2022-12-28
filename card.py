class Card:
    def __init__(self, name, suit, value, color='black'):
        self.name = name
        self.suit = suit
        self.value = value
        self.color = color

    def __str__(self):
        return f'{self.name}{self.suit}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name == other.name and self.suit == other.suit and self.value == other.value

