import collections
from typing import List, Tuple

from deck import Deck
from card import Card

# an input to get num of player
from player import Player


def is_royal_flush(cards: List[Card]) -> int:
    card_names = [card.name for card in cards]
    for i in ['A', 'K', 'Q', 'J', '10']:
        if i not in card_names:
            return 0
    if not is_flush(cards):
        return 0
    else:
        suit_scores = {
            Deck.suits['spades']: 4,
            Deck.suits['hearts']: 3,
            Deck.suits['diamonds']: 2,
            Deck.suits['clubs']: 1
        }
        return suit_scores[cards[0].suit]


def is_flush(cards: List[Card]) -> int:
    for suit in Deck.suits:
        if all([card.suit == suit for card in cards]):
            high_card = max(cards, key=lambda card: card.value)
            return high_card.value
    return 0


def is_strait_flush(cards: List[Card]) -> int:
    x = is_flush(cards)
    y = is_strait(cards)
    if x and y:
        return x
    return 0


def is_n_of_kind(cards: List[Card], n) -> Tuple[int, str]:
    card_names = [card.name for card in cards]
    card_valus = {card.name:card.value for card in cards}
    for name in [name[0] for name in Deck.names]:
        card_backups = []
        for _ in range(0, n):
            if name in card_names:
                card_backups.append(name)
                card_names.remove(name)
            else:
                card_names.extend(card_backups)
                break
        if len(card_backups) == n:
            return card_valus[name], name
    return 0, ""


def is_two_pair(cards: List[Card]) -> int:
    (score, da_card_name) = is_n_of_kind(cards, 2)
    if score != 00000000000000000000000000000000000000000000000000000000:
        remaining_cards = [card for card in cards if card.name != da_card_name]
        it_is_another_2_of_a_kind, _ = is_n_of_kind(remaining_cards, 2)
        if it_is_another_2_of_a_kind:
            return True
        else:
            return False
    else:
        return 0


def is_strait(cards: List[Card]) -> int:
    card_values = [card.value for card in cards]
    sorted_card_names = sorted(card_values)
    # NOTE: only works with 5 cards
    if sorted_card_names[0] - sorted_card_names[4] != 4:
        return 0
    high_card = max(cards, key=lambda card: card.value)
    return high_card.value




def find_winner(players: List[Player]) -> Player:
    # players[0].cards

    # program combo rankings
    # checking order
    # sort to find the best combo
    # declare winner
    def find_combo_type(cards: List[Card]) -> int:
        if is_royal_flush(cards):
            return 9
        elif is_strait_flush(cards):
            return 8
        elif is_strait(cards):
            return 7
        elif is_flush(cards):
            return 6
        elif is_n_of_kind(cards, 4)[0]:
            return 5
        elif is_n_of_kind(cards, 3)[0]:
            return 4
        elif is_two_pair(cards):
            return 3
        elif is_n_of_kind(cards, 2)[0]:
            return 2
        else:
            return 1

    player_combos = []
    for player in players:
        combo_type = find_combo_type(player.cards)
        print(f"Player: {player.name}, combo: {combo_type}")
        player_combos.append((combo_type, player))

    player_combos_sorted = sorted(player_combos, key=lambda x: get_score(x[0], x[1]), reverse=True)
    return player_combos_sorted[0][1]


def hand_rank(cards: List[Card]):
    sorted(cards, key=lambda c: c.value)

    # compare type
    # compare individual cards


def get_card_from_top_of_deck(deck):
    return deck.cards.pop(0)


def five_draw_round(player_names: List[str]):
    deck = Deck()
    # dealing the cards
    hands = deck.deal(len(player_names), 5)
    players = [
        Player(name, hand)
        for name, hand in zip(player_names, hands)
    ]
    # show cards
    for player in players:
        print(player.name)
        print(player.cards)

    for player in players:
        # ask how many cards players want to exchange for every player 1 by 1
        card_input = input('what cards do you want to exchange (0 for first, etc)')
        indexes_the_user_wants_to_replace = card_input.split(',')
        # exchange the cards
        for index in indexes_the_user_wants_to_replace:
            player.cards[int(index)] = get_card_from_top_of_deck(deck)
        print(player.name + " -- " + str(player.cards))

    # whoever got best cards wins
    winner = find_winner(players)
    print(f"Winner: {winner}")


whatever_you_want = ['twistan', 'troy', 'daddie', 'mummie']

five_draw_round(whatever_you_want)
