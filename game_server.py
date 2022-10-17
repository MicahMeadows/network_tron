
import asyncio
from xmlrpc.client import MAXINT
import websockets
from random import randint

class GameServer:
    '''class for creating a server'''
    def __init__(self) -> None:
        self.users = []
        self.PORT = 8080
    
    async def start(self):
        '''start the server up'''
        async with websockets.serve(self.listen, "localhost", self.PORT):
            print(f"running on {self.PORT}")
            await asyncio.Future()

    async def listen(self, websocket):
        '''method that will listen for new messages'''
        async for message in websocket:
            print(f"got message: {message}")
            if message == "get user":
                random_id = randint(0, MAXINT)
                print(f'randID: {random_id}')
                await websocket.send(f"{random_id}")