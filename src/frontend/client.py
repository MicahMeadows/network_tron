'''client websocket module'''

import asyncio
from curses import erasechar
import json
from dataclasses_json import dataclass_json
import websockets
from src.common.message import Message


class Client:
    def __init__(self, url):
        self.url: str = url
        self.message_handlers = { }
        self.connection = None

    async def connect(self):
        async with websockets.connect(self.url, ping_interval=None) as websocket:
            self.connection = websocket
            user = await self.get_user()
            await self.listen()

    async def get_user(self):
        create_user_id_message = Message("create-new-user-id", "")
        create_user_id_message_json = create_user_id_message.to_json()
        await self.connection.send(create_user_id_message_json)

    def change_direction(self, new_direction):
        new_direction_message = Message("player-change-direction", new_direction)
        new_direction_message_json = new_direction_message.to_json()
        asyncio.run(self.connection.send(new_direction_message_json))

    def register_message_handler(self, label, fn):
        self.message_handlers[label] = fn

    async def listen(self):
        while True:
            message = await self.connection.recv()
            try:
                message = Message.from_json(message)
                try:
                    message_handler = self.message_handlers[message.label]
                    message_handler(message.body_json)
                except:
                    print(f'failed to get message handler for ({message.label})')
            except:
                print('error parsing messages')

            