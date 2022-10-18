'''tron game logic'''

import curses
import time
from src.common.coordinate import Coordinate

from src.common.player import MoveDirection, Player
from src.common.player_dto import PlayerDTO

class TronGame:
    def __init__(self):
        self.on_get_players = None
        self.on_player_move = None
        self.CLOSE_KEY = 27
        self.key = curses.KEY_RIGHT
        self.render_delay = .1
        self.next_render = time.time()
        self.waiting_for_players = False

        self.score_a = 0
        self.score_b = 0

        self.window_size = {
            "rows": 20,
            "columns": 80
        }

        # setup window
        curses.initscr()
        curses.noecho()
        curses.curs_set(0)

        self.window = curses.newwin(self.window_size["rows"], self.window_size["columns"], 0, 0) # y, x
        self.window.keypad(1)
        self.window.nodelay(1)

    def set_waiting_for_players(self, is_waiting):
        self.waiting_for_players = is_waiting

    def set_on_get_players(self, on_get_players):
        self.on_get_players = on_get_players

    def set_on_player_move(self, on_player_move):
        self.on_player_move = on_player_move

        
    def get_score_string(self):
        return f'({self.score_a},{self.score_b})'

    def draw_title_string(self):
        self.window.addstr(0, 2, "Tron")

    def draw_waiting_message(self):
        self.window.addstr(5, 5, "Waiting for players...")

    def draw_score_string(self):
        score_string = self.get_score_string()
        score_x_offset = (self.window_size["columns"] // 2 - 1) - (len(score_string) // 2)
        self.window.addstr(0, score_x_offset, score_string)

    def get_new_key(self) -> int:
        new_key: int = self.window.getch()

        if new_key in [
            curses.KEY_LEFT,
            curses.KEY_RIGHT,
            curses.KEY_UP,
            curses.KEY_DOWN,
            self.CLOSE_KEY
        ]:
            return new_key

    def polar_to_curses_coordinate(self, polar: Coordinate) -> Coordinate:
        x_fix = polar.x
        y_fix = self.window_size["rows"] - 1 - polar.y
        return Coordinate(x_fix, y_fix)

    def render_player(self, player: PlayerDTO):
        for pos in player.positions:
            curses_coords = self.polar_to_curses_coordinate(pos)
            try:
                self.window.addch(curses_coords.y, curses_coords.x, str(player.display_character) if player.is_alive else 'X')
            except:
                pass

    def run(self):
        while self.key != self.CLOSE_KEY:
            
            key = self.get_new_key()

            move_direction: MoveDirection = None
            match key:
                case curses.KEY_RIGHT:
                    move_direction = MoveDirection.RIGHT
                case curses.KEY_LEFT:
                    move_direction = MoveDirection.LEFT
                case curses.KEY_UP:
                    move_direction = MoveDirection.UP
                case curses.KEY_DOWN:
                    move_direction = MoveDirection.DOWN
            
            if move_direction:
                self.on_player_move(move_direction)

            current_time = time.time()
            if current_time > self.next_render:
                self.next_render = current_time + self.render_delay
                self.window.erase()
                self.window.border(0)

                self.draw_title_string()
                self.draw_score_string()

                if self.waiting_for_players:
                    self.draw_waiting_message()
                    self.set_waiting_for_players(False)

                players: list[PlayerDTO] = list(self.on_get_players())
                for player in players:
                    self.render_player(player)

                self.window.refresh()
        curses.endwin()
        print("good game")