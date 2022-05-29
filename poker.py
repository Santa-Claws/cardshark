from copy import copy
from typing import List, Tuple

from deck import Deck
from card import Card

# an input to get num of player
from player import Player

ZERO_SCORE = tuple([0 for _ in range(5)])


def sorted_by_value(cards):
    return tuple(sorted([card.value for card in cards], reverse=True))


def is_royal_flush(cards: List[Card]) -> Tuple:
    card_names = [card.name for card in cards]
    for i in ['A', 'K', 'Q', 'J', '10']:
        if i not in card_names:
            return ZERO_SCORE
    if not is_flush(cards):
        return ZERO_SCORE
    else:
        suit_scores = {
            Deck.suits['spades']: 4,
            Deck.suits['hearts']: 3,
            Deck.suits['diamonds']: 2,
            Deck.suits['clubs']: 1
        }
        return tuple([suit_scores[cards[0].suit]] + [0 for _ in range(4)])


def is_flush(cards: List[Card]) -> Tuple:
    for suit in Deck.suits.values():
        if all([card.suit == suit for card in cards]):
            return sorted_by_value(cards)
    return ZERO_SCORE


def is_strait_flush(cards: List[Card]) -> Tuple:
    x = is_flush(cards)
    y = is_strait(cards)
    if x[0] and y[0]:
        return x
    return ZERO_SCORE


def is_n_of_kind(cards: List[Card], n) -> Tuple[Tuple, str]:
    card_names = [card.name for card in cards]
    card_valus = {card.name: card.value for card in cards}
    for name in [name[0] for name in Deck.names]:
        card_backups = []
        for _ in range(0, n):
            if name in card_names:
                card_backups.append(name)
                card_names.remove(name)
            else:
                # high_cards = copy(card_names)
                card_names.extend(card_backups)
                break
        if len(card_backups) == n:
            return tuple([card_valus[z] for z in card_backups] + sorted([card_valus[z] for z in card_names], reverse=True)), name
    return ZERO_SCORE, ""


def is_two_pair(cards: List[Card]) -> Tuple:
    (score, da_card_name) = is_n_of_kind(cards, 2)
    if score[0] != 0:
        remaining_cards = [card for card in cards if card.name != da_card_name]
        (score_2, da_other_card_name) = is_n_of_kind(remaining_cards, 2)
        if score_2[0] != 0:
            ordered_scores = score_2[0:2] + score[0:2] if score_2[0] > score[0] else score[0:2] + score_2[0:2]
            remaining_cards = [card for card in remaining_cards if card.name != da_other_card_name]
            return ordered_scores + tuple([card.value for card in remaining_cards])
        else:
            return ZERO_SCORE
    else:
        return ZERO_SCORE


def is_strait(cards: List[Card]) -> Tuple:
    card_values = [card.value for card in cards]
    sorted_card_names = sorted(card_values)
    # NOTE: only works with 5 cards
    if sorted_card_names[0] - sorted_card_names[4] != 4:
        return ZERO_SCORE
    return sorted_by_value(cards)


def high_card(cards: List[Card]) -> Tuple:
    return sorted_by_value(cards)


def find_winner(players: List[Player]) -> Player:
    # players[0].cards
    import functools
    list_of_functions = [
        (is_royal_flush, "royal flush"),
        (is_strait_flush, "straight flush"),
        (is_strait, "straight"),
        (is_flush, "flush"),
        (functools.partial(is_n_of_kind, n=4), "4 of a kind"),
        (functools.partial(is_n_of_kind, n=3), "3 of a kind"),
        (is_two_pair, "two pair"),
        (functools.partial(is_n_of_kind, n=2), "pair"),
        (high_card, "high card")
    ]
    # returns (combo_type, scores) tuple
    def find_combo_type(cards: List[Card]) -> Tuple:
        for count, function in enumerate([f[0] for f in list_of_functions]):
            score = function(cards=cards)
            score = score[0] if isinstance(score[0], Tuple) else score
            if score[0]:
                # the combo type is descending values
                return (len(list_of_functions) - count,) + score

    combo_name_lookup = {
        (len(list_of_functions) - combo[0]): combo[1][1]
        for combo in enumerate(list_of_functions)
    }
    player_combos = []
    for player in players:
        combo_type = find_combo_type(player.cards)
        print(f"Player: {player.name}, combo: {combo_name_lookup[combo_type[0]]} {combo_type}")
        player_combos.append((combo_type, player))

    player_combos_sorted = sorted(player_combos, reverse=True)
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
        indexes_the_user_wants_to_replace = card_input.split(',') if card_input.strip() else []
        # exchange the cards
        for index in indexes_the_user_wants_to_replace:
            player.cards[int(index)] = get_card_from_top_of_deck(deck)
        print(player.name + " -- " + str(player.cards))

    # whoever got best cards wins
    winner = find_winner(players)
    print(f"Winner: {winner}")


whatever_you_want = ['twistan', 'troy', 'daddie', 'mummie']

five_draw_round(whatever_you_want)
