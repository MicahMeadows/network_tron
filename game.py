'''tron game logic'''

import curses
import time

from player import MoveDirection, Player

class TronGame:
    def __init__(self):
        self.CLOSE_KEY = 27
        self.key = curses.KEY_RIGHT

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

        
    def get_score_string(self):
        return f'({self.score_a},{self.score_b})'

    def draw_title_string(self):
        self.window.addstr(0, 2, "Tron")

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

    def polar_to_curses_coordinate(self, polar):
        x_fix = polar[0]
        y_fix = self.window_size["rows"] - 1 - polar[1]
        return (x_fix, y_fix)

    def render_player(self, player: Player):
        for pos in player.trail:
            curses_coords = self.polar_to_curses_coordinate(pos)
            try:
                self.window.addch(curses_coords[1], curses_coords[0], player.display_char)
            except:
                pass

    def run(self):
        player = Player('#', 'Micah',  6, 6, MoveDirection.RIGHT)

        while self.key != self.CLOSE_KEY:
            self.window.erase()
            self.window.border(0)

            self.draw_title_string()
            self.draw_score_string()

            key = self.get_new_key()

            moveDirection: MoveDirection = None
            match key:
                case curses.KEY_RIGHT:
                    moveDirection = MoveDirection.RIGHT
                case curses.KEY_LEFT:
                    moveDirection = MoveDirection.LEFT
                case curses.KEY_UP:
                    moveDirection = MoveDirection.UP
                case curses.KEY_DOWN:
                    moveDirection = MoveDirection.DOWN
            
            if moveDirection:
                player.set_direction(moveDirection)

            player.move()

            self.render_player(player)

            self.window.refresh()
            curses.napms(100)
        curses.endwin()
        print("good game")