import sys
import websockets

import asyncio
import threading

from src.common.message import Message
from src.backend.backend_game import BackendGame
from src.backend.game_server import GameServer
from src.backend.server_controller import ServerController
from src.common.coordinate import Coordinate
from src.common.game_state import GameState
from src.common.player import Player
from src.common.player_dto import PlayerDTO

class ServerThread(threading.Thread):
    def __init__(self, server: GameServer):
        self.server = server
        threading.Thread.__init__(self)
    
    def run(self):
        server_start_task = self.server.start()
        asyncio.run(server_start_task)

class GameUpdateThread(threading.Thread):
    def __init__(self, server_controller: ServerController):
        self.server_controller = server_controller
        threading.Thread.__init__(self)

    @staticmethod
    def create_player_dto(player: Player):
        coordinates = list(map(lambda pos : Coordinate(x=pos[0], y=pos[1]), player.trail))
        return PlayerDTO(display_character=player.display_char, positions=coordinates, is_alive=player.alive)

    def run(self):
        while True:
            self.server_controller.backend_game.move_players()

            players = list(map(lambda socket_player : socket_player.player, self.server_controller.socket_players))
            player_dtos = list(map(lambda player : self.create_player_dto(player), players))

            game_state: GameState = GameState(player_dtos)
            game_state_json = game_state.to_json()
            game_state_message = Message("game-state-update", game_state_json)
            game_state_message_json = game_state_message.to_json()

            for socket_player in self.server_controller.socket_players:
                try:
                    task = socket_player.socket.send(game_state_message_json)
                    asyncio.run(task)
                except:
                    self.server_controller.disconnect_player(socket_player)

async def main():
    backend_game = BackendGame((80, 20))
    server = GameServer()

    server_thread = ServerThread(server)
    server_controller = ServerController(backend_game, server)
    game_update_thread = GameUpdateThread(server_controller)

    server_thread.start()
    game_update_thread.start()

    server_thread.join()
    game_update_thread.join()

asyncio.run(main())