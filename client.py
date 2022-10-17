'''client websocket module'''

import asyncio
import websockets


class Client:
    def __init__(self, url):
        self.url: str = url
        self.connection = None

    async def connect(self):
        async with websockets.connect(self.url) as websocket:
            self.connection = websocket
            user = await self.get_user()

    async def get_user(self):
        await self.connection.send("get user")
        user = await self.connection.recv()
        print(user)
