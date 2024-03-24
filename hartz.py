import json
import selectors
import traceback
from time import sleep
from typing import List, Tuple
import card
from card import Card
from deck import Deck
from player import Player
from random import randint


def get_played_index(played, index):
    return next(i for i, p in enumerate(played) if p[0] == index)


def game_flow(players):
    hart_staus = False
    current_player_index = find_three_clubs(players)

    for i in range(0, 13):
        lead_card = None

        cards_played = []
        for j in range(len(players)):
            if hart_staus == False:
                for c in cards_played:
                    if c[2].suit == Deck.suits['hearts']:
                        hart_staus = True
            forst_hond = (i == 0)
            current_player = players[current_player_index]
            current_player.sort_hearts()
            card_played = play_card(cards_played, current_player, lead_card, hart_staus, forst_hond)
            if j == 0:
                lead_card = card_played
            cards_played.append((current_player_index, players[current_player_index], card_played))
            current_player_index = (current_player_index + 1) % len(players)

        current_player_index = leader(cards_played, lead_card)
        print( " Trick: ", ''.join(['{:>4}'.format(str(c[2])) for c in cards_played]))
        print(f"           {'    '*get_played_index(cards_played, current_player_index)}↑")
        print("Trick winner: ", players[current_player_index].name)

        players[current_player_index].trick_cards.extend(cards_played)
        print(players[current_player_index].trick_cards)
    # round is over
    for player in players:
        for _, _, card in player.trick_cards:
            if card.suit == '♥':
                player.score += 1
            elif card.suit == '♠' and card.value == 13:
                player.score += 13


    for player in players:
        if player.score == 26:
            for playerr in players:
                if not playerr.name == player.name:
                    playerr.score += 26
            player.score -= 26
            break
    for player in players:
        print(f"Player: {player.name} Score: {player.score}")

def game_flow_remote(players, sel):
    hart_staus = False
    current_player_index = find_three_clubs(players)

    for i in range(0, 13):
        lead_card = None

        cards_played = []
        for j in range(len(players)):
            if hart_staus == False:
                for c in cards_played:
                    if c[2].suit == Deck.suits['hearts']:
                        hart_staus = True
            forst_hond = (i == 0)
            current_player = players[current_player_index]
            current_player.sort_hearts()
            card_played = play_card_remote(sel, players, cards_played, current_player, lead_card, hart_staus, forst_hond)
            if j == 0:
                lead_card = card_played
            cards_played.append((current_player_index, players[current_player_index], card_played))
            current_player_index = (current_player_index + 1) % len(players)

        current_player_index = leader(cards_played, lead_card)
        print("Trick winner: ", players[current_player_index]['name'])

def find_three_clubs(players):
    playerindex = 0
    for player in players:
        for c in player.cards:
            if c.suit == Deck.suits['clubs'] and c.value == 3:
                return playerindex
        playerindex += 1


def leader(player_and_card: List[Tuple], lead_card):
    # if card not same suit then kill th0em immediately
    # else then compare numbers and hui0ghest wins, kill the rest
    def suit_same(player_and_card_tuple: Tuple):
        return lead_card.suit == player_and_card_tuple[2].suit

    cards_with_the_special_one_and_only_lead_suit = filter(suit_same, player_and_card)

    def value_vinnnnnnnnnnnnnnnnnnnnnnnnnner(player_and_card_tuple: Tuple):
        return player_and_card_tuple[2].value

    vinner = max(cards_with_the_special_one_and_only_lead_suit, key=value_vinnnnnnnnnnnnnnnnnnnnnnnnnner)
    return vinner[0]


# use input validation for playable cards
def if_card_allowed(card: Card, lead_card: Card, hond: List[Card], hart_staus: bool, forst_hond: bool):
    hond_suits = set([c.suit for c in hond])
    if lead_card is None:
        # first player of hand
        if forst_hond:
            return card.suit == Deck.suits['clubs'] and card.value == 3
        if card.suit == Deck.suits['hearts']:
            if hart_staus:
                return True
            else:
                # can only break hearts if have no other suits
                for s in hond_suits:
                    if s != Deck.suits['hearts']:
                        return False
        return True
    if forst_hond:
        if card.suit == Deck.suits['hearts'] or (card.name == 'Q' and card.suit == Deck.suits['spades']):
            # no point cards on first hand
            return False
    if card.suit == lead_card.suit:
        return True
    else:
        return lead_card.suit not in hond_suits


def ai(lead_card: Card, hond: List[Card], hart_staus: bool, forst_hond: bool):
    while True:
        card = hond[randint(0, (len(hond) - 1))]
        if if_card_allowed(card, lead_card, hond, hart_staus, forst_hond):
            return card


    #for c in hond:
        #if if_card_allowed(c, lead_card, hond, hart_staus, forst_hond):
            #return c
    #raise RuntimeError('no valid card!!! ')


def play_card(cards_played: List[Tuple[int, Player, Card]], player: Player, lead_card, hart_staus, forst_hond):
    while True:
        print("        -------------------------")
        print(" Trick: |", ''.join(['{:>4}'.format(str(c[2])) for c in cards_played]), " |")
        print("        -------------------------")
        print(f'\n\n{player.name}\n')
        print(''.join(["{:>3}{}".format(c.name, c.suit) for c in player.cards]))
        print(''.join(["{0:4}".format(idx) for idx in range(len(player.cards))]))
        if player.ai:
            card = ai(lead_card, player.cards, hart_staus, forst_hond)
        else:
            card_input = input('wat card do u wanna play\n(0 for first, etc)\n')
            card = player.cards[int(card_input)]
        if if_card_allowed(card, lead_card, player.cards, hart_staus, forst_hond):
            player.cards.remove(card)
            return card
        else:
            print("Card not allowed")


def play_card_remote(sel, players, cards_played: List[Tuple[int, Player, Card]], player: Player, lead_card, hart_staus, forst_hond):
    game_state = GameState(
        lead_card=lead_card,
        hart_staus=hart_staus,
        forst_hond=forst_hond,
        whos_turn=player.name
    )
    print(f"Sending game state information to player: {player.name}")
    for player in players:
        print(f"Player={player}")
        players_game_state = json.dumps({**game_state, **{"player_name": player.name}})
        msg = player.message._create_message(
            content_bytes=players_game_state.encode(),
            content_type="text/json",
            content_encoding="utf-8"
        )
        print(msg)
        player.message.sock.send(msg)
    sleep(1)
    while True:
        print(" Trick: ", [c[2] for c in cards_played])
        print(f'\n\n{player.name}\n')
        print(''.join(["{:>3}{}".format(c.name, c.suit) for c in player.cards]))
        print(''.join(["{0:4}".format(idx) for idx in range(len(player.cards))]))
        card_played = wait_for_card_played(sel)
        card = player.cards[int(card_played)]
        if if_card_allowed(card, lead_card, player.cards, hart_staus, forst_hond):
            player.cards.remove(card)
            return card
        else:
            print("Card not allowed")


def wait_for_card_played(sel):
    while True:
        sleep(1)
        print("Waiting in loop..")
        sock, addr = None, None
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data:
                message = key.data
                try:
                    card_played = {}
                    def read_card(data):
                        if "card_played" in data:
                            card_played["index"] = int(data["card_played"])
                    message.process_events(mask, read_card)
                    ### Check here ^ for played card, not seeing it yet
                    if "index" in card_played:
                        return card_played["index"]
                except Exception:
                    print(
                        f"Main: Error: Exception for {message.addr}:\n"
                        f"{traceback.format_exc()}"
                    )
                    message.close()



if __name__ == "__main__":
    player_names = ['bob', 'alice', 'leeroy', 'cletis']
    while True:
        deck = Deck()
        hands = deck.deal(len(player_names), 13)
        players = [
            Player(name, hand, ai=True)
            for name, hand in zip(player_names, hands)
        ]
        game_flow(players)
        if len(list(filter(lambda p: p.score == 26, players))) > 0:
            break

# second player picks what clubs they want to play
# if no clubs the have player pick card of their choice
# if card o' choice is hearts then break hearts
# when hearts break then players are allowed to lead with hearts
# second - 4 players doe same, following same condition
# player with the highest clubs move in play cards to their take pile variable
# once done then player places a card of their choice and cycle continues until 13 rounds is done
# once thirteen rounds done then count take pile
# each heart in pile adds 1 to player points
# player with queen o' spades gains thirteen points
# player with least points wins

#weight point system for rules
# if have queen of spades,last in trick,leader, or first round then diffrent set of rules
#rules
#play highest card below top card
#want to get rid of sauits
#if dont have any of lead card suit then play highest card prioritizing hearts
#if all cards higheeer than lead card play lowest card
# if nothing to lose then play higherst card
# if lead then play lowest card and target getting rid of suits
# if someone trying to shoot moon then wait to take one point

#queen rules
# play cards higher than queen

#leader rules
#if queen hasnt been played and have only spades below queen then play spades
#play lowest card targwetting getting riud of suits also if all cards for that suit are gone then dont play it
#if have queen thewn dont play queen
#dont play high hearts


#last rules
#if nothing to lose then play highest card other than queen
#target getting ridf of suits
#

#card passing rules
#get rid of highest hearts
#get rid of highest cards
#target getting rid of a suit
#almost never get rid of spades
#if only have queen of spades or less than 2 other spades the pass it
# if have 2 or fewer of same suit the getr rid