import json
from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard

@dataclass
class Card(JSONWizard):
    def __init__(self, name, suit, value, color='black'):
        self.name = name
        self.suit = suit
        self.value = value
        self.color = color

    def serialize(self):
        attributes_for_card = {'name': self.name, 'suit': self.suit, 'value': self.value, 'color': self.color}
        return json.dumps(attributes_for_card)

    @staticmethod
    def deserialize(serialized_json):
        card_attrs = json.loads(serialized_json)
        return Card(
            name=card_attrs['name'],
            suit=card_attrs['suit'],
            value=card_attrs['value'],
            color=card_attrs['color']
        )

    def __str__(self):
        return f'{self.name}{self.suit}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name == other.name and self.suit == other.suit and self.value == other.value

    def __lt__(self, other):
        return self.value < other.value
