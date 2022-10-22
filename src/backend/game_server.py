import asyncio
from xmlrpc.client import MAXINT
import websockets
from src.common.message import Message
import src.common.proto_compiled.message as proto_message

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
                    try:
                        message_json = Message.from_json(message)
                        try:
                            message_handler = self.message_handlers[message_json.label]
                            message_handler(websocket, message_json.body)
                        except:
                            raise Exception(f'failed to get message handler for ({message_json.label})')
                    except Exception as e:
                        print(f'Failure to handle as json message: {e}')

                    try:
                        message_proto = proto_message.Message().FromString(message)
                        try:
                            message_handler = self.message_handlers[message_proto.label]
                            message_handler(websocket, message_proto.body)
                        except Exception as e:
                            raise Exception(f'failed to get message handler for ({message_proto.label})')
                    except Exception as e:
                        print(f'Failure to handle message as proto buf: {e}')
                except Exception as e:
                    print(f'Failed to parse message: {e}')
        except:
            try:
                self.users.remove(websocket)
            except:
                pass