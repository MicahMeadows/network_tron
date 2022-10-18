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
    
    def run(self):
        self.server_controller.game_loop()

    

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