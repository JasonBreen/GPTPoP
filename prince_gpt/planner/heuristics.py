from __future__ import annotations

from prince_gpt.core.schemas import GameState


def x_distance_to_exit(state: GameState, exit_x: int) -> int:
    return abs(exit_x - state.prince.position.x)
