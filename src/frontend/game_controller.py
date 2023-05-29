from ast import literal_eval
import asyncio
from src.common.coordinate import Coordinate
from src.common.game_state import GameState
from src.common.player_dto import PlayerDTO
from src.frontend import curses_tron_game
from src.frontend.client import Client
# from src.frontend.curses_tron_game import CursesTronGame

import src.common.proto_compiled.tron_game as proto_tron_game
from src.frontend.tron_game import TronGame

class TronGameController:
    def __init__(self, tron_game: TronGame, client: Client):
        self.tron_game = tron_game
        self.client = client
        self.setup_message_handlers()
        self.setup_game_methods()
        self.current_game_state: GameState = None
        self.waiting_for_players = False

    def setup_message_handlers(self):
        self.client.register_message_handler('game-state-update', self.game_state_update_message_handler)
        self.client.register_message_handler('new-user-id', self.new_user_id_message_handler)
        self.client.register_message_handler('waiting-for-players', self.waiting_for_players_message_handler)

    def setup_game_methods(self):
        self.tron_game.set_on_get_players(self.get_players)
        self.tron_game.set_on_player_move(self.player_move)

    def player_move(self, direction):
        self.client.change_direction(direction)
    
    def get_players(self):
        if self.current_game_state is None:
            return []

        return self.current_game_state.players


    @staticmethod
    def coordinate_from_proto(proto) -> Coordinate:
        return Coordinate(x=proto.x, y=proto.y)

    @staticmethod
    def player_dto_from_proto(proto) -> PlayerDTO:
        return PlayerDTO(
            display_character=proto.display_character,
            is_alive=proto.is_alive,
            positions=list(map(TronGameController.coordinate_from_proto, proto.positions))
        )

    @staticmethod
    def game_state_from_proto(game_state_proto) -> GameState:
        return GameState(players=list(map(TronGameController.player_dto_from_proto, game_state_proto.players)))
    
    def game_state_update_message_handler(self, game_state_data_str):
        game_state_data_str = literal_eval(game_state_data_str)
        new_game_state_proto = proto_tron_game.GameState().parse(game_state_data_str)
        new_game_state = TronGameController.game_state_from_proto(new_game_state_proto)

        self.current_game_state = new_game_state

    def waiting_for_players_message_handler(self, body):
        self.tron_game.set_waiting_for_players(True)

    def new_user_id_message_handler(self, user_id_json):
        pass
    