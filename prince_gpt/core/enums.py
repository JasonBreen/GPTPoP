from __future__ import annotations

from enum import Enum


class TileKind(str, Enum):
    EMPTY = "empty"
    FLOOR = "floor"
    WALL = "wall"
    GAP = "gap"
    SPIKES = "spikes"
    GATE = "gate"
    PRESSURE_PLATE = "pressure_plate"
    LOOSE_FLOOR = "loose_floor"
    EXIT = "exit"


class Direction(str, Enum):
    LEFT = "left"
    RIGHT = "right"


class Pose(str, Enum):
    STANDING = "standing"
    RUNNING = "running"
    HANGING = "hanging"
    CLIMBING = "climbing"
    FALLING = "falling"
    DEAD = "dead"


class ActionName(str, Enum):
    WAIT = "wait"
    STEP_LEFT = "step_left"
    STEP_RIGHT = "step_right"
    RUN_LEFT = "run_left"
    RUN_RIGHT = "run_right"
    STANDING_JUMP_LEFT = "standing_jump_left"
    STANDING_JUMP_RIGHT = "standing_jump_right"
    RUNNING_JUMP_LEFT = "running_jump_left"
    RUNNING_JUMP_RIGHT = "running_jump_right"
    CLIMB_UP = "climb_up"
    DROP_AND_HANG = "drop_and_hang"
