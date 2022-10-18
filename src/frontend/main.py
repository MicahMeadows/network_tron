import asyncio
from threading import Thread
from src.frontend.client import Client
from src.frontend.game_controller import TronGameController
from src.frontend.tron_game import TronGame

async def main():
    '''main composition method'''
    url = "ws://localhost:8080"

    client = Client(url)
    game = TronGame()
    game_controller = TronGameController(game, client)

    game_thread = GameThread(game)
    network_thread = NetworkThread(client)

    game_thread.start()
    network_thread.start()

    game_thread.join()
    network_thread.join()

class GameThread(Thread):
    def __init__(self, game: TronGame):
        self.game = game
        Thread.__init__(self)

    def run(self):
        self.game.run()

class NetworkThread(Thread):
    def __init__(self, client: Client):
        self.client = client
        Thread.__init__(self)

    def run(self):
        asyncio.run(self.client.connect())

asyncio.run(main())