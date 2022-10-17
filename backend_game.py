from ast import List
from player import MoveDirection, Player


class BackendGame:
    def __init__(self) -> None:
        self.players: List[Player] = []

    def set_player_direction(self, player_name, new_direction: MoveDirection):
        for player in self.players:
            if player.player_name == player_name:
                player.set_direction(new_direction)

    def move_players(self):
        for player in self.players:
            player.move()
