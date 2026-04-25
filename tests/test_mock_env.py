from prince_gpt.core.enums import ActionName, Pose
from prince_gpt.env.mock_env import MockPrinceEnv


def test_mock_env_reset_starts_left_not_done() -> None:
    env = MockPrinceEnv()
    state = env.reset()
    assert state.prince.position.x == 1
    assert state.done is False


def test_step_right_into_gap_kills_prince() -> None:
    env = MockPrinceEnv()
    env.reset()
    env.step(ActionName.STEP_RIGHT)  # x=2
    env.step(ActionName.STEP_RIGHT)  # x=3

    result = env.step(ActionName.STEP_RIGHT)  # x=4 gap => death
    assert result.success is False
    assert result.failure_type == "fell_or_impaled"
    assert result.new_state.prince.pose == Pose.DEAD
    assert result.new_state.done is True


def test_running_jump_right_crosses_gap_from_correct_spot() -> None:
    env = MockPrinceEnv()
    env.reset()
    env.step(ActionName.STEP_RIGHT)  # x=2
    env.step(ActionName.STEP_RIGHT)  # x=3

    result = env.step(ActionName.RUNNING_JUMP_RIGHT)
    assert result.success is True
    assert result.new_state.prince.position.x == 5
    assert result.new_state.prince.pose == Pose.STANDING
