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

