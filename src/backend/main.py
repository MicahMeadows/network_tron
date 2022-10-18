import sys


import asyncio

from src.backend.backend_game import BackendGame
from src.backend.game_server import GameServer
from src.backend.server_controller import ServerController


async def main():
    backend_game = BackendGame((80, 20))
    server = GameServer()

    server_controller = ServerController(backend_game, server)

    await server_controller.start()

asyncio.run(main())