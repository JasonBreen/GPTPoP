from __future__ import annotations

import heapq
from dataclasses import dataclass, field

from prince_gpt.core.enums import ActionName
from prince_gpt.env.base_env import BasePrinceEnv
from prince_gpt.env.mock_env import MockPrinceEnv
from prince_gpt.planner.heuristics import x_distance_to_exit


@dataclass(order=True)
class _Node:
    priority: int
    cost: int
    x: int = field(compare=False)
    actions: list[ActionName] = field(compare=False, default_factory=list)


class AStarPlanner:
    def __init__(self, max_expansions: int = 200) -> None:
        self.max_expansions = max_expansions

    def _extract_exit_x(self, env: BasePrinceEnv) -> int:
        state = env.get_state()
        room = state.rooms[state.prince.position.room_id]
        for x in range(room.width):
            if room.tile_at(x, state.prince.position.y).kind.value == "exit":
                return x
        raise ValueError("No EXIT tile found in room")

    def _candidate_actions(self) -> list[ActionName]:
        return [
            ActionName.STEP_RIGHT,
            ActionName.RUN_RIGHT,
            ActionName.RUNNING_JUMP_RIGHT,
        ]

    def plan(self, env: BasePrinceEnv) -> list[ActionName]:
        if not isinstance(env, MockPrinceEnv):
            raise TypeError("AStarPlanner currently expects MockPrinceEnv for simulation")

        start_state = env.get_state()
        if start_state.done:
            return []
        exit_x = self._extract_exit_x(env)

        start_x = start_state.prince.position.x
        heap: list[_Node] = []
        heapq.heappush(
            heap,
            _Node(
                priority=x_distance_to_exit(start_state, exit_x),
                cost=0,
                x=start_x,
                actions=[],
            ),
        )
        best_cost: dict[int, int] = {start_x: 0}
        expansions = 0

        while heap and expansions < self.max_expansions:
            node = heapq.heappop(heap)
            expansions += 1

            sim_env = env.clone()
            sim_env.reset()
            for a in node.actions:
                sim_env.step(a)

            current_state = sim_env.get_state()
            if current_state.done:
                return node.actions

            for action in self._candidate_actions():
                branch_env = sim_env.clone()
                result = branch_env.step(action)
                if not result.success:
                    continue
                if result.new_state.prince.pose.value == "dead":
                    continue

                new_x = result.new_state.prince.position.x
                new_cost = node.cost + 1
                prev_best = best_cost.get(new_x)
                if prev_best is not None and new_cost >= prev_best:
                    continue

                best_cost[new_x] = new_cost
                h = x_distance_to_exit(result.new_state, exit_x)
                heapq.heappush(
                    heap,
                    _Node(
                        priority=new_cost + h,
                        cost=new_cost,
                        x=new_x,
                        actions=node.actions + [action],
                    ),
                )

        return []
