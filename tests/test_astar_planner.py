from prince_gpt.env.mock_env import MockPrinceEnv
from prince_gpt.planner.astar import AStarPlanner


def test_astar_finds_route_to_exit() -> None:
    env = MockPrinceEnv()
    env.reset()
    planner = AStarPlanner()

    plan = planner.plan(env)

    assert plan, "planner should produce a non-empty plan"

    sim = env.clone()
    sim.reset()
    for action in plan:
        result = sim.step(action)
        assert result.success, f"action failed during rollout: {action}"

    assert sim.get_state().done is True
