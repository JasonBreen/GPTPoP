from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from prince_gpt.core.enums import ActionName, Direction, Pose, TileKind


class Position(BaseModel):
    room_id: str
    x: int
    y: int


class Tile(BaseModel):
    kind: TileKind
    walkable: bool = True
    deadly: bool = False


class Room(BaseModel):
    width: int
    height: int
    tiles: list[Tile]

    def tile_at(self, x: int, y: int) -> Tile:
        idx = y * self.width + x
        return self.tiles[idx]


class PrinceState(BaseModel):
    position: Position
    facing: Direction
    pose: Pose
    hp: int = 3
    has_sword: bool = False


class GameState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=False)

    level_id: str
    prince: PrinceState
    rooms: dict[str, Room]
    time_remaining: int
    done: bool = False


class ActionResult(BaseModel):
    success: bool
    previous_state: GameState
    action: ActionName
    new_state: GameState
    failure_type: Optional[str] = None
    frames: int = 0
    reward: float = 0.0


class TransitionRecord(BaseModel):
    state_before: GameState
    action: ActionName
    state_after: GameState
    success: bool
    failure_type: Optional[str] = None
    reward: float = 0.0
    frames: int = 0


def make_tile(kind: TileKind) -> Tile:
    if kind == TileKind.GAP:
        return Tile(kind=kind, walkable=False, deadly=True)
    if kind == TileKind.SPIKES:
        return Tile(kind=kind, walkable=False, deadly=True)
    if kind == TileKind.WALL:
        return Tile(kind=kind, walkable=False, deadly=False)
    return Tile(kind=kind, walkable=True, deadly=False)
