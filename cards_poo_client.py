import json
import selectors
import socket

from card import Card
from player import Player

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 1025  # The port used by the server

#sel = selectors.DefaultSelector()

def deal_to_player(name: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world, das ist guuuuut")
    data = s.recv(1024*10)
    parsed_hand = json.loads(data.decode())
    deserialized_cards = []
    for card in parsed_hand:
        deserialized_cards.append(Card.deserialize(card))
    my_player = Player(name="frivle", cards=deserialized_cards, socket=s)
    print(f"My dealt cards ({name}: {my_player.cards}")
    return my_player


def run_player(player: Player):
    #events = sel.select(timeout=None)
    data = player.socket.recv(1024*100)
    print(f"Data={data}")
    if not data:
        print(f"No data for {player.name}")
        return
    parssed_data = json.loads(data.decode())
    print(parssed_data)
    if parssed_data['whos_turn'] == player.name:
        card_index = input("Which card to play? >")
        print("Waiting for more..")
        encoded_card_index = card_index.encode()
        player.socket.send(encoded_card_index)


p1 = deal_to_player("twistan")
p2 = deal_to_player("twoy")
p3 = deal_to_player("daddie")
p4 = deal_to_player("mommy")
players = [p1, p2, p3, p4]

#for player in players:
#    sel.register(player.socket, selectors.EVENT_READ, data=None)

while True:
    for player in players:
        run_player(player)
