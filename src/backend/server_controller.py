import asyncio
from curses.panel import update_panels
from email import message
from xmlrpc.client import Server
from random import randint
import random

import src.common.proto_compiled.player_dto_pb2 as player_dto_pb2
import src.common.proto_compiled.coordinate_pb2 as coordinate_pb2
import src.common.proto_compiled.message_pb2 as message_pb2
import src.common.proto_compiled.game_state_pb2 as game_state_pb2

import websockets
from src.common.coordinate import Coordinate
from src.common.game_state import GameState

from dataclasses_json import dataclass_json

from src.common.player import MoveDirection, Player
from src.common.player_dto import PlayerDTO
from .game_server import GameServer
from .backend_game import BackendGame
from src.common.message import Message

class SocketPlayer:
    def __init__(self, player: Player, socket):
        self.player = player
        self.socket = socket
    

class ServerController:
    def __init__(self, backend_game: BackendGame, server: GameServer):
        self.backend_game = backend_game
        self.server = server
        self.socket_players = []
        self.game_update_thread = None
        self.register_message_handlers()
        self.server.set_on_new_connection(lambda connection : self.add_socket_player(self.create_random_player(), connection))

    def disconnect_player(self, player: SocketPlayer):
        self.socket_players.remove(player)
        self.update_players()

    def register_message_handlers(self):
        self.server.register_message_handler("create-new-user-id", self.create_new_user_id_message_handler)
        self.server.register_message_handler("player-change-direction", self.player_change_direction_message_handler)

    def player_change_direction_message_handler(self, sender, direction_string):
        new_dir = MoveDirection(direction_string)
        for socket_player in self.socket_players:
            if socket_player.socket == sender:
                self.backend_game.set_player_direction(socket_player.player.name, new_dir)

    def create_new_user_id_message_handler(self, sender, body):
        print(f'({sender.local_address}) asked for new id')
    
    def update_players(self):
        player_list = list(map(lambda socket_player : socket_player.player, self.socket_players))
        self.backend_game.set_players(player_list)

    def create_random_player(self) -> Player:
        display_char = len(self.socket_players)

        start_x = randint(5, self.backend_game.game_size[0] - 5)
        start_y = randint(5, self.backend_game.game_size[1] - 5)

        new_player = Player(display_char, f"player {display_char}", start_x, start_y, random.choice(list(MoveDirection)))
        return new_player

    def add_socket_player(self, player: Player, connection):
        new_socket_player = SocketPlayer(player, connection)
        self.socket_players.append(new_socket_player)
        self.update_players()

    @staticmethod
    def create_player_dto(player: Player):
        coordinates = list(map(lambda pos : Coordinate(x=pos[0], y=pos[1]), player.trail))
        return PlayerDTO(display_character=player.display_char, positions=coordinates, is_alive=player.alive)

    @staticmethod
    def create_coordinate_proto(coordinate: Coordinate) -> coordinate_pb2.Coordinate:
        new_proto = coordinate_pb2.Coordinate()
        new_proto.x = coordinate.x
        new_proto.y = coordinate.y
        return new_proto
    
    @staticmethod
    def create_player_dto_proto(player_dto: PlayerDTO) -> player_dto_pb2.PlayerDTO():
        new_proto = player_dto_pb2.PlayerDTO()
        new_proto.is_alive = player_dto.is_alive
        new_proto.display_character = str(player_dto.display_character)

        coordinate_protos = list(map(ServerController.create_coordinate_proto, player_dto.positions))
        new_proto.positions.extend(coordinate_protos)
        return new_proto

    @staticmethod
    def create_game_state_proto(game_state: GameState) -> game_state_pb2.GameState():
        new_proto = game_state_pb2.GameState()
        new_proto_players = list(map(ServerController.create_player_dto_proto, game_state.players))
        new_proto.players.extend(new_proto_players)
        return new_proto

    @staticmethod
    def create_message_proto(message: Message) -> message_pb2.Message():
        new_proto = message_pb2.Message()
        new_proto.label = message.label
        new_proto.body = str(message.body)
        return new_proto

    def game_loop(self):
        while True:
            if len(self.socket_players) >= 2:
                self.backend_game.move_players()
            else:
                player_connections = list(map(lambda socket_player: socket_player.socket, self.socket_players))
                
                waiting_message_proto = message_pb2.Message()
                waiting_message_proto.label = "waiting-for-players"
                waiting_message_proto.body = str(2 - len(self.socket_players))

                waiting_message_data_str = waiting_message_proto.SerializeToString()
                websockets.broadcast(player_connections, waiting_message_data_str)


            # get list of players for game state
            players = list(map(lambda socket_player : socket_player.player, self.socket_players))
            player_dtos = list(map(self.create_player_dto, players))

            # create game state and serialize it to a string for message
            game_state: GameState = GameState(player_dtos)
            game_state_proto = self.create_game_state_proto(game_state)
            game_state_data_str = game_state_proto.SerializeToString()

            # create message for state update
            game_state_message = Message("game-state-update", str(game_state_data_str))
            game_state_message_proto = self.create_message_proto(game_state_message)
            game_state_message_data_str = game_state_message_proto.SerializeToString()

            connections = list(map(lambda socket_player: socket_player.socket, self.socket_players))
            websockets.broadcast(connections, game_state_message_data_str)

            # for socket_player in self.socket_players:
            #     try:
            #         task = socket_player.socket.send(game_state_message_data_str)
            #         asyncio.run(task)
            #     except:
            #         self.disconnect_player(socket_player)

    # idk do something with this
    def close(self):
        if self.game_update_thread is not None:
            self.game_update_thread.join()