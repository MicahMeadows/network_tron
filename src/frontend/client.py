'''client websocket module'''

from curses import erasechar
import dataclasses
from dataclasses_json import dataclass_json
import json
import websockets
from src.common.message import Message


class Client:
    def __init__(self, url):
        self.url: str = url
        self.connection = None

    async def connect(self):
        async with websockets.connect(self.url) as websocket:
            self.connection = websocket
            user = await self.get_user()
            await self.listen()

    async def get_user(self):
        await self.connection.send("create-new-user-id")

    async def listen(self):
        while True:
            message = await self.connection.recv()
            try:
                message = Message.from_json(message)
                if message.label == "game-state-update":
                    print('got a game update')
                elif message.label == "new-user-id":
                    print(f'new id: {message.body_json}')
                else:
                    print(message)
            except:
                print('error parsing messages')

            