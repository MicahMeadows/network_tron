from enum import Enum

class MoveDirection(Enum):
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    UP = "UP"
    DOWN = "DOWN"
    
class Player(object):
    def __init__(self, display_char, name, start_x_position, start_y_position, start_move_direction):
        self.display_char = display_char
        self.name = name
        self.x = start_x_position
        self.y = start_y_position
        self.move_direction = start_move_direction
        self.trail = []
        self.alive = True
        self.last_move = None

    @staticmethod
    def opposite_direction(direction: MoveDirection):
        try:
            return {
                MoveDirection.RIGHT: MoveDirection.LEFT,
                MoveDirection.LEFT: MoveDirection.RIGHT,
                MoveDirection.UP: MoveDirection.DOWN,
                MoveDirection.DOWN: MoveDirection.UP
            }[direction]
        except:
            return None


    def set_direction(self, new_direction: MoveDirection):
        if self.opposite_direction(self.last_move) != new_direction:
            self.move_direction = new_direction

    def kill(self):
        self.alive = False
    
    def move(self):
        if (self.alive):
            self.trail.append((self.x, self.y))
            match self.move_direction:
                case MoveDirection.LEFT:
                    self.x -= 1
                case MoveDirection.RIGHT:
                    self.x += 1
                case MoveDirection.UP:
                    self.y += 1
                case MoveDirection.DOWN:
                    self.y -= 1
            self.last_move = self.move_direction
