import functools
import json
import selectors
import socket
import traceback

from card import Card
from player import Player
from poo_game import Game
from client_message import Message

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 1025  # The port used by the server

sel = selectors.DefaultSelector()

game = Game()

def connect_to_server(name: str):
    addr = (HOST, PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    request = {
        "type": "text/json",
        "encoding": "utf-8",
        "content": {"player_name": name},
    }
    message = Message(sel, sock, addr, request)
    sel.register(sock, events, data=message)


def uber_function(game, data):
    if 'dealt_cards' in data:
        get_dealt_cards(game, data)
    if 'lead_card' in data:
        run_player(game, data)


def get_dealt_cards(game, data):
    if "dealt_cards" not in data:
        print(f"Not a dealt hand response: {data}")
        return
    deserialized_cards = []
    for card in data["dealt_cards"]:
        deserialized_cards.append(Card.deserialize(card))
    my_player = Player(name=data["player_name"], cards=deserialized_cards)
    print(f"My dealt cards {sorted(my_player.cards)}")
    game.players[my_player.name] = my_player
    return None


def run_player(game, data):
    print(f"Data={data}")
    if not data:
        print(f"No data ")
        return
    if 'player_name' in data:
        player = game.players[data['player_name']]
        if data['whos_turn'] == player.name:
            card_index = input("Which card to play? >")
            return {"card_played": card_index}


p1 = connect_to_server("twistan")
p2 = connect_to_server("twoy")
p3 = connect_to_server("daddie")
p4 = connect_to_server("mommy")
players = [p1, p2, p3, p4]

try:
    while True:
        print("Waiting for events")
        events = sel.select(timeout=None)
        print(f"Events: {events}")
        for key, mask in events:
            message = key.data
            try:
                uber_fun = functools.partial(uber_function, game=game)
                message.process_events(mask=mask, data_processing_function=uber_fun)
            except Exception:
                print(
                    f"Main: Error: Exception for {message.addr}:\n"
                    f"{traceback.format_exc()}"
                )
                message.close()
            # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()


