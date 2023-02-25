import json
import sys
import socket
import selectors
import types
from typing import Tuple, Any

from deck import Deck
from hartz import game_flow_remote
from player import Player
from poo_game import Game

def main(host, port):
    game = Game()
    deck = Deck()
    num_players = 4
    hands = deck.deal(num_players, 13)
    sel = selectors.DefaultSelector()
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((host, port))
    lsock.listen()
    print(f"Listening on {(host, port)}")
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)
    try:
        deal_cards(game, hands, num_players, sel)
        game_flow_remote(players=list(game.players.values()), sel=sel)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()


def deal_cards(game, hands, num_players, sel):
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(sel, key.fileobj)
            else:
                service_connection(sel, key, mask, game, hands)
        if len(game.players) == num_players:
            print("All players ready")
            return


def add_player(addr, game, hands, key):
    current_player = len(game.players)
    player_name = f"player{current_player}"
    print(f"Players: {game.players}")
    game.players[addr] = Player(name=player_name, cards=hands[current_player], socket=key.fileobj)
    serialized_cards = json.dumps([card.serialize() for card in hands[current_player]])
    key.fileobj.send(serialized_cards.encode())


def accept_wrapper(sel, sock) -> tuple[Any, Any]:
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    return sock, addr


def service_connection(sel, key, mask, game, hands):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print("Received data")
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Adding player (data={data.outb!r} to {data.addr}")
            add_player(data.addr, game, hands, key)
            sent = sock.send(b"Play your card!")  # Should be ready to write
            data.outb = data.outb[sent:]


if __name__ == '__main__':
    main(host='', port=int(sys.argv[2]))

#alwayse send information to player even if its not thier turn
#all players get constant state update