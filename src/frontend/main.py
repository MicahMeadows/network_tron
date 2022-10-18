import asyncio
from src.frontend.client import Client
from src.frontend.game_controller import TronGameController
from src.frontend.tron_game import TronGame

async def main():
    '''main composition method'''
    url = "ws://localhost:8080"

    client = Client(url)
    game = TronGame()
    game_controller = TronGameController(game, client)

    await game_controller.start()

asyncio.run(main())