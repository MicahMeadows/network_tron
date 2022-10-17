from enum import Enum

class MoveDirection(Enum):
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    UP = "UP"
    DOWN = "DOWN"
    

class Player:
    def __init__(self, display_char, name, start_x_position, start_y_position, start_move_direction):
        self.display_char = display_char
        self.name = name
        self.x = start_x_position
        self.y = start_y_position
        self.move_direction = start_move_direction
        self.trail = []
    
    def set_direction(self, newDirection: MoveDirection):
        self.move_direction = newDirection

    def move(self):
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