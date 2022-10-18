import asyncio
from src.common.game_state import GameState
from src.frontend import tron_game
from src.frontend.client import Client
from src.frontend.tron_game import TronGame

class TronGameController:
    def __init__(self, tron_game: TronGame, client: Client):
        self.tron_game = tron_game
        self.client = client
        self.setup_message_handlers()
        self.setup_game_methods()
        self.current_game_state_json: str = None
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
        if self.current_game_state_json is None: # return empty is no current state loaded
            return []

        current_game_state = GameState.from_json(self.current_game_state_json)
        return current_game_state.players
    
    def game_state_update_message_handler(self, game_state_json):
        self.current_game_state_json = game_state_json

    def waiting_for_players_message_handler(self, body_json):
        self.tron_game.set_waiting_for_players(True)

    def new_user_id_message_handler(self, user_id_json):
        pass
    