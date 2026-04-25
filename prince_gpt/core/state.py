from __future__ import annotations

from copy import deepcopy

from prince_gpt.core.schemas import GameState


def clone_state(state: GameState) -> GameState:
    return deepcopy(state)
