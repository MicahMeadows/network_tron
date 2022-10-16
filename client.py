'''client websocket module'''

import asyncio
import websockets


class Client:
    '''client class'''

    def __init__(self):
        self.connection = None

    async def connect(self, URL):
        '''connect to server'''
        async with websockets.connect(URL) as websocket:
            self.connection = websocket
            await self.get_user()

    async def get_user(self):
        await self.connection.send("get user")

    async def diconnect(self):
        await self.connection.send("disconnect")
    
    async def on_message(self, event):
        print(f'message: {event.data}')

    async def on_error(self, error):
        print(f'error: {error}')

async def main():
    '''main composition method'''
    url = "ws://localhost:8080"
    client = Client()
    await client.connect(url)

asyncio.run(main())
