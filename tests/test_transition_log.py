from prince_gpt.core.enums import ActionName
from prince_gpt.core.schemas import TransitionRecord
from prince_gpt.data.transition_log import TransitionLogger
from prince_gpt.env.mock_env import MockPrinceEnv


def test_transition_logger_round_trip_jsonl(tmp_path) -> None:
    env = MockPrinceEnv()
    before = env.reset()
    result = env.step(ActionName.STEP_RIGHT)

    record = TransitionRecord(
        state_before=before,
        action=ActionName.STEP_RIGHT,
        state_after=result.new_state,
        success=result.success,
        failure_type=result.failure_type,
        reward=result.reward,
        frames=result.frames,
    )

    logger = TransitionLogger()
    logger.append(record)

    path = tmp_path / "transitions.jsonl"
    logger.save_jsonl(path)

    loaded = TransitionLogger.load_jsonl(path)
    assert len(loaded.records) == 1
    assert loaded.records[0].action == ActionName.STEP_RIGHT
    assert loaded.records[0].state_after.prince.position.x == 2
