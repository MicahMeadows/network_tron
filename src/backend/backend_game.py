
from ast import List
from os import kill
from subprocess import check_output
from src.common.coordinate import Coordinate
from src.common.player import MoveDirection, Player
import time

class BackendGame:
    def __init__(self, game_size) -> None:
        self.players: list[Player] = []
        self.game_size = game_size
        self.move_delay = .4
        self.next_move = time.time()

    def set_players(self, players):
        self.players = players

    def set_player_direction(self, player_name, new_direction: MoveDirection):
        for player in self.players:
            if player.name == player_name:
                player.set_direction(new_direction)

    def move_players(self):
        current_time = time.time()
        if current_time >= self.next_move:
            self.next_move = current_time + self.move_delay
            for player in self.players:
                player.move()
                self.check_players()

    def check_players(self):
        kill_spots: list[Coordinate] = []
        for player in self.players:
            for trail_piece in player.trail:
                piece_coordinate: Coordinate = Coordinate(trail_piece[0], trail_piece[1])
                kill_spots.append(piece_coordinate)
        
        for player in self.players:
            player_coord = Coordinate(player.x, player.y)

            over_x = player_coord.x >= self.game_size[0] - 1
            under_x = player_coord.x < 1
            over_y = player_coord.y >= self.game_size[1] - 1
            under_y = player_coord.y < 1

            out_of_boudns = over_x or under_x or over_y or under_y
            if out_of_boudns:
                player.kill()

            hit_snake = player_coord in kill_spots
            if hit_snake:
                player.kill()
