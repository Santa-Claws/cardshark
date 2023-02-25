import functools
import json
import sys
import socket
import selectors
import traceback
import types
from typing import Tuple, Any

from deck import Deck
from hartz import game_flow_remote
from player import Player
from poo_game import Game
from server_message import Message


def accept_wrapper(sel, sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    message = Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)


def main(host, port):
    game = Game()
    deck = Deck()
    num_players = 4
    game.hands = deck.deal(num_players, 13)
    sel = selectors.DefaultSelector()
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Avoid bind() exception: OSError: [Errno 48] Address already in use
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind((host, port))
    lsock.listen()
    print(f"Listening on {(host, port)}")
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    try:
        deal_cards(game, num_players, sel)
        game_flow_remote(players=list(game.players.values()), sel=sel)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()


def deal_cards(game, num_players, sel):
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(sel, key.fileobj)
            else:
                message = key.data
                add_player2 = functools.partial(
                    add_player, game=game, message=message
                )
                try:
                    message.process_events(mask, add_player2)
                except Exception:
                    print(
                        f"Main: Error: Exception for {message.addr}:\n"
                        f"{traceback.format_exc()}"
                    )
                    message.close()

        if len(game.players) == num_players:
            print("All players ready")
            return


def add_player(game, message, data):
    current_player = len(game.players)
    player_name = data["player_name"]
    print(f"Player name: {player_name}")
    game.players[player_name] = Player(
        name=player_name, cards=game.hands[current_player], message=message
    )
    print(f"Added to Players: {game.players}")
    return {
        "player_name": player_name,
        "dealt_cards": [
            card.serialize() for card in game.hands[current_player]
        ]
    }


if __name__ == '__main__':
    main(host='', port=int(sys.argv[2]))

#alwayse send information to player even if its not thier turn
#all players get constant state update