from deck import Deck
from player import Player


def play_round(players, is_war=False):
    round = [(player, player.cards.pop(0)) for player in players]
    played_cards = [card[1] for card in round]
    print("Round: ", round)
    if is_war:
        print('Its war..', round)
        return None, played_cards
    tie = all(card[1].value == round[0][1].value for card in round)
    if tie:
        print("Tie: ", round, " This means WAR!")
        return None, played_cards
    winner = max(round, key=lambda p: p[1].value)
    print("Winner: ", winner[0].name, winner[1])
    return winner[0].name, played_cards


if __name__ == "__main__":
    deck = Deck()
    #deck.print()
    hands = deck.deal(2, 26)
    players = [Player(name, cards) for name, cards in zip(["tristan", "troy"], hands)]
    for player in players:
        print(f"\nPlayer {player.name}:")
        for i in range(0, len(player.cards), 13):
            [print(f"{str(card)}, ", end="") for card in player.cards[i:i + 13]]
            print()

    cards_on_table = []
    num_rounds, war_rounds = 0, 0
    while all(len(player.cards) > 0 for player in players):
        [print(f"{player.name:10}", [card for card in player.cards]) for player in players]
        winner, played_cards = play_round(players)
        cards_on_table.extend(played_cards)
        if winner:
            list(filter(lambda p: p.name == winner, players))[0].cards.extend(cards_on_table)
            cards_on_table.clear()
        else:
            for _ in range(3):
                _, additional_cards = play_round(players, is_war=True)
                cards_on_table.extend(additional_cards)
            war_rounds += 1
        print()
        num_rounds += 1
        #sleep(1)
    print(f'Game over... in {num_rounds} rounds with {war_rounds} WAR rounds\n')
    [print(player, player.cards) for player in players]
