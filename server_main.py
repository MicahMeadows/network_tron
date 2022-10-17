
import asyncio

from backend.backend_game import BackendGame
from backend.game_server import GameServer
from backend.server_controller import ServerController


async def main():
    backend_game = BackendGame()
    server = GameServer()

    server_controller = ServerController(backend_game, server)

    await server_controller.start()

if __name__ == "__main__":
    asyncio.run(main())