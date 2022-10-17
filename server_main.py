import asyncio

from backend_game import BackendGame
from game_server import GameServer
from server_controller import ServerController

async def main():
    backend_game = BackendGame()
    server = GameServer()

    server_controller = ServerController(backend_game, server)

    await server_controller.start()

asyncio.run(main())