from backend_game import BackendGame
from game_server import GameServer

class ServerController:
    def __init__(self, backend_game: BackendGame, server: GameServer):
        self.backend_game = backend_game
        self.server = server
    
    async def start(self):
        await self.server.start()