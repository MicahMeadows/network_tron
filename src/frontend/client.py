'''client websocket module'''

from email import message
import src.common.proto_compiled.message_pb2 as message_pb2
import asyncio
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
        create_user_id_message = message_pb2.Message()
        create_user_id_message.label = "create-new-user-id"
        create_user_id_message.body = ""

        create_user_id_message_string = create_user_id_message.SerializeToString()

        await self.connection.send(create_user_id_message_string)

    def change_direction(self, new_direction):
        new_direction_message = message_pb2.Message()
        new_direction_message.label = "player-change-direction"
        new_direction_message.body = str(new_direction.value)
        new_direction_message_data_str = new_direction_message.SerializeToString()
        task = self.connection.send(new_direction_message_data_str)
        asyncio.run(task)
        # new_direction_message = Message("player-change-direction", new_direction)
        # new_direction_message_json = new_direction_message.to_json()
        # asyncio.run(self.connection.send(new_direction_message_json))

    def register_message_handler(self, label, fn):
        self.message_handlers[label] = fn

    async def listen(self):
        while True:
            message = await self.connection.recv()
            json_fail = ""
            proto_fail = ""
            try:
                try: # try to parse as json
                    json_message = Message.from_json(message)
                    try:
                        message_handler = self.message_handlers[json_message.label]
                        message_handler(json_message.body)
                    except:
                        raise Exception(f'failed to get message handler for ({json_message.label})')
                except Exception as e:
                    json_fail = f'Failed to parse as json: {e}'
                
                try: # try to parse as proto buf
                    proto_message = message_pb2.Message().FromString(message)
                    message_handler = self.message_handlers[proto_message.label]
                    message_handler(proto_message.body)
                except Exception as e:
                    proto_fail = f'Failed to parse as proto: {e}'
                
                if json_fail != "" and proto_fail != "":
                    raise Exception(f'Failed to parse: ({json_fail}, {proto_fail})')
            except Exception as e:
                print(f'error parsing messages: {e}')

            