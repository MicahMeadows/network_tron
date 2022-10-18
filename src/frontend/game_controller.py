from src.frontend.client import Client
from src.frontend.tron_game import TronGame

class TronGameController:
    def __init__(self, tron_game: TronGame, client: Client):
        self.tron_game = tron_game
        self.client = client

    async def start(self):
        await self.client.connect()