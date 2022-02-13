from enum import Enum, auto
from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.QtCore import Qt

SPRAY_BOTTLE_SIZE = (18, 33)
GUN_SIZE = (25, 25)
SNACK_DISPENSER_SIZE = (25, 40)
LITTER_BOX_SIZE = (70, 40)
POOP_SIZE = (15, 15)
SNACK_SIZE = (15, 15)

class Dir(Enum):
    UP    = 0
    DOWN  = 1
    LEFT  = 2
    RIGHT = 3
    UP_RIGHT   = 4
    UP_LEFT    = 5
    DOWN_RIGHT = 6
    DOWN_LEFT  = 7
    NORTH = UP
    SOUTH = DOWN
    EAST  = RIGHT
    WEST  = LEFT
    NORTH_WEST = UP_LEFT
    NORTH_EAST = UP_RIGHT
    SOUTH_WEST = DOWN_LEFT
    SOUTH_EAST = DOWN_RIGHT


class State(Enum):
    WALKING = auto()
    PAWING  = auto()
    YAWNING = auto()
    POOPING = auto()
    SITTING = auto()
    SLEEPING = auto()
    WAKING_UP = auto()
    FALLING_ASLEEP = auto()


class Mission(Enum):
    WANDER = auto()
    FOLLOW_MOUSE = auto()
    FOLLOW_MOUSE_CLICKS = auto()
    WANDER_EDGE = auto()
    WANDER_EDGE_VAUGE = auto()
    WANDER_WINDOW = auto()
