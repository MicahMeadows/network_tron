import asyncio
from xmlrpc.client import MAXINT
import websockets
from random import randint
import threading
import time
from src.common.message import Message

class GameServer:
    '''class for creating a server'''
    def __init__(self) -> None:
        self.on_new_connection = None
        self.users= []
        self.PORT = 8080
        self.message_handlers = {}

    def register_message_handler(self, message, fn):
        self.message_handlers[message] = fn

    def set_on_new_connection(self, method):
        self.on_new_connection = method

    async def start(self):
        '''start the server up'''
        async with websockets.serve(self.listen, "localhost", self.PORT):
            print(f"running on {self.PORT}")
            await asyncio.Future()
    
    async def listen(self, websocket):
        if not websocket in self.users:
            self.users.append(websocket)
            if self.on_new_connection is not None:
                print(f'new connection: {websocket.local_address}')
                self.on_new_connection(websocket)

        try:
            async for message in websocket:
                try:
                    message = Message.from_json(message)
                    try:
                        message_handler = self.message_handlers[message.label]
                        message_handler(websocket, message.body_json)
                    except:
                        print(f'failed to get message handler for ({message.label})')
                except:
                    print('error parsing messages')
        except:
            try:
                self.users.remove(websocket)
            except:
                pass