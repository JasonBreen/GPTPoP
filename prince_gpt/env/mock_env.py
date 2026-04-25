from __future__ import annotations

from copy import deepcopy

from prince_gpt.core.actions import all_actions
from prince_gpt.core.enums import ActionName, Direction, Pose, TileKind
from prince_gpt.core.schemas import ActionResult, GameState, Position, PrinceState, Room, make_tile
from prince_gpt.env.base_env import BasePrinceEnv


class MockPrinceEnv(BasePrinceEnv):
    """Deterministic one-room mock environment.

    Layout (x):
    0 1 2 3 4 5 6 7 8 9
    F F F F G F F F E F

    Start at x=1. Gap at x=4. Exit at x=8.
    RUNNING_JUMP_RIGHT works only from x=3 and lands at x=5.
    """

    def __init__(self) -> None:
        self._initial_state = self._build_initial_state()
        self._state = deepcopy(self._initial_state)

    def _build_initial_state(self) -> GameState:
        width = 10
        height = 1
        row = [TileKind.FLOOR] * width
        row[4] = TileKind.GAP
        row[8] = TileKind.EXIT
        tiles = [make_tile(kind) for kind in row]
        room = Room(width=width, height=height, tiles=tiles)
        prince = PrinceState(
            position=Position(room_id="room-1", x=1, y=0),
            facing=Direction.RIGHT,
            pose=Pose.STANDING,
            hp=3,
            has_sword=False,
        )
        return GameState(
            level_id="mock-level-1",
            prince=prince,
            rooms={"room-1": room},
            time_remaining=300,
            done=False,
        )

    def clone(self) -> MockPrinceEnv:
        cloned = MockPrinceEnv()
        cloned._state = deepcopy(self._state)
        cloned._initial_state = deepcopy(self._initial_state)
        return cloned

    def reset(self) -> GameState:
        self._state = deepcopy(self._initial_state)
        return self.get_state()

    def get_state(self) -> GameState:
        return deepcopy(self._state)

    def is_done(self) -> bool:
        return self._state.done

    def available_actions(self) -> list[ActionName]:
        return all_actions()

    def _tile_kind_at(self, x: int) -> TileKind:
        room = self._state.rooms[self._state.prince.position.room_id]
        if x < 0 or x >= room.width:
            return TileKind.WALL
        return room.tile_at(x, self._state.prince.position.y).kind

    def _dead_result(self, previous: GameState, action: ActionName, failure_type: str) -> ActionResult:
        new_state = deepcopy(self._state)
        new_state.prince.pose = Pose.DEAD
        new_state.prince.hp = 0
        new_state.done = True
        self._state = deepcopy(new_state)
        return ActionResult(
            success=False,
            previous_state=previous,
            action=action,
            new_state=deepcopy(new_state),
            failure_type=failure_type,
            frames=12,
            reward=-1.0,
        )

    def _move_step(self, dx: int, action: ActionName) -> ActionResult:
        previous = self.get_state()
        state = self._state
        target_x = state.prince.position.x + dx
        tile_kind = self._tile_kind_at(target_x)

        if tile_kind in {TileKind.WALL, TileKind.GATE}:
            return ActionResult(
                success=False,
                previous_state=previous,
                action=action,
                new_state=self.get_state(),
                failure_type="blocked",
                frames=6,
                reward=-0.1,
            )

        if tile_kind in {TileKind.GAP, TileKind.SPIKES}:
            return self._dead_result(previous, action, failure_type="fell_or_impaled")

        state.prince.position.x = target_x
        state.prince.facing = Direction.RIGHT if dx > 0 else Direction.LEFT
        state.prince.pose = Pose.STANDING
        state.time_remaining -= 1
        if tile_kind == TileKind.EXIT:
            state.done = True
        return ActionResult(
            success=True,
            previous_state=previous,
            action=action,
            new_state=self.get_state(),
            frames=6,
            reward=1.0 if state.done else 0.1,
        )

    def _run_jump_right(self) -> ActionResult:
        previous = self.get_state()
        state = self._state
        x = state.prince.position.x

        if x != 3:
            return ActionResult(
                success=False,
                previous_state=previous,
                action=ActionName.RUNNING_JUMP_RIGHT,
                new_state=self.get_state(),
                failure_type="bad_jump_setup",
                frames=10,
                reward=-0.2,
            )

        # Jump over x=4 gap and land at x=5.
        if self._tile_kind_at(4) != TileKind.GAP:
            return ActionResult(
                success=False,
                previous_state=previous,
                action=ActionName.RUNNING_JUMP_RIGHT,
                new_state=self.get_state(),
                failure_type="gap_missing",
                frames=10,
                reward=-0.2,
            )

        landing_tile = self._tile_kind_at(5)
        if landing_tile in {TileKind.WALL, TileKind.GATE, TileKind.GAP, TileKind.SPIKES}:
            return self._dead_result(previous, ActionName.RUNNING_JUMP_RIGHT, failure_type="bad_landing")

        state.prince.position.x = 5
        state.prince.facing = Direction.RIGHT
        state.prince.pose = Pose.STANDING
        state.time_remaining -= 2
        if landing_tile == TileKind.EXIT:
            state.done = True

        return ActionResult(
            success=True,
            previous_state=previous,
            action=ActionName.RUNNING_JUMP_RIGHT,
            new_state=self.get_state(),
            frames=12,
            reward=0.2,
        )

    def step(self, action: ActionName) -> ActionResult:
        if self._state.done:
            return ActionResult(
                success=False,
                previous_state=self.get_state(),
                action=action,
                new_state=self.get_state(),
                failure_type="episode_done",
            )

        if action == ActionName.WAIT:
            prev = self.get_state()
            self._state.time_remaining -= 1
            return ActionResult(
                success=True,
                previous_state=prev,
                action=action,
                new_state=self.get_state(),
                frames=1,
                reward=0.0,
            )
        if action == ActionName.STEP_RIGHT:
            return self._move_step(dx=1, action=action)
        if action == ActionName.STEP_LEFT:
            return self._move_step(dx=-1, action=action)
        if action == ActionName.RUN_RIGHT:
            return self._move_step(dx=1, action=action)
        if action == ActionName.RUN_LEFT:
            return self._move_step(dx=-1, action=action)
        if action == ActionName.RUNNING_JUMP_RIGHT:
            return self._run_jump_right()

        return ActionResult(
            success=False,
            previous_state=self.get_state(),
            action=action,
            new_state=self.get_state(),
            failure_type="unsupported_action_in_mock",
            frames=1,
            reward=-0.05,
        )
