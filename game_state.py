import json
from dataclasses import dataclass, field
from typing import List

from dataclass_wizard import JSONWizard

from card import Card


class Game:
    def __init__(self):
        self.players = {}
        self.hands = []


class GameState:
    def __init__(self, phase, whos_turn, lead_card, hart_staus, forst_hond):
        self.phase = phase #dealing, trick
        self.whos_turn = whos_turn
        self.lead_card = lead_card
        self.hart_staus = hart_staus
        self.forst_hond = forst_hond
        self.card_played = None

    def serialize(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def deserialize(serialized_json: str):
        game_attrs = json.loads(serialized_json)
        return GameState(
            phase=game_attrs["phase"],
            whos_turn=game_attrs["whos_turn"],
            lead_card=game_attrs["lead_card"],
            hart_staus=game_attrs["hart_staus"],
            forst_hond=game_attrs["forst_hond"]
        )


@dataclass
class HeartsRoundState(JSONWizard):
    round_number: int = 1
    cards_in_trick: list[Card] = field(default_factory=list)
    card_played: Card = None
    lead_card: Card = None
    player_order: int = None
    hearts_broken: bool = False
    queen_played: bool = False

    def record(self):
        with open('data.jsonl', 'a') as f:
            f.write(json.dumps(self.to_json()) + "\n")
