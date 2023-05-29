import asyncio
from threading import Thread
from src.frontend import game_controller
from src.frontend.client import Client
from src.frontend.curses_tron_game import CursesTronGame
from src.frontend.game_controller import TronGameController
from src.frontend.pygame_tron_game import PygameTronGame
from src.frontend.tron_game import TronGame

# class GameThread(Thread):
#     def __init__(self, game: TronGame):
#         self.game = game
#         Thread.__init__(self)

#     def run(self):
#         self.game.run()


class NetworkThread(Thread):
    def __init__(self, client: Client):
        self.client = client
        Thread.__init__(self)

    def run(self):
        asyncio.run(self.client.connect())

async def main():
    '''main composition method'''

    client: Client = Client("ws://localhost:8080")
    # game = CursesTronGame()
    game: TronGame = PygameTronGame()

    controller: TronGameController  = TronGameController(game, client)

    # game_thread = GameThread(game)
    network_thread = NetworkThread(client)

    # game_thread.start()
    network_thread.start()

    game.run()

    # game_thread.join()
    network_thread.join()

asyncio.run(main())