from __future__ import annotations

from prince_gpt.core.enums import ActionName
from prince_gpt.core.schemas import ActionResult
from prince_gpt.env.base_env import BasePrinceEnv


class MacroExecutor:
    """Thin execution wrapper for environment macro-actions."""

    def __init__(self, env: BasePrinceEnv) -> None:
        self.env = env

    def execute(self, action: ActionName) -> ActionResult:
        return self.env.step(action)
