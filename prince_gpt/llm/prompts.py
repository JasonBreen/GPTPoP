from __future__ import annotations

CHOOSE_NEXT_ACTION_PROMPT = """
You are choosing the next macro-action for Prince.
Given structured state and available macro-actions, return one action name.
Prioritize survival and progress toward the exit.
""".strip()

REPAIR_FAILED_PLAN_PROMPT = """
A planned macro-action failed.
Given state, attempted plan, and failure reason, propose a repaired plan.
Keep the plan short and deterministic.
""".strip()

SUMMARIZE_FAILURE_PROMPT = """
Summarize the failure trajectory in plain language.
Include likely root cause and one concrete next correction.
""".strip()
