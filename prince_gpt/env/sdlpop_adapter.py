from __future__ import annotations

from prince_gpt.core.enums import ActionName
from prince_gpt.core.schemas import ActionResult, GameState
from prince_gpt.env.base_env import BasePrinceEnv


class SDLPoPAdapter(BasePrinceEnv):
    """Placeholder adapter for future SDLPoP integration."""

    def reset(self) -> GameState:
        raise NotImplementedError("SDLPoP integration is not implemented yet")

    def get_state(self) -> GameState:
        raise NotImplementedError("SDLPoP integration is not implemented yet")

    def step(self, action: ActionName) -> ActionResult:
        raise NotImplementedError("SDLPoP integration is not implemented yet")

    def available_actions(self) -> list[ActionName]:
        raise NotImplementedError("SDLPoP integration is not implemented yet")

    def is_done(self) -> bool:
        raise NotImplementedError("SDLPoP integration is not implemented yet")
