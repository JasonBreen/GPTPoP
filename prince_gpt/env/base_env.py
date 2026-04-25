from __future__ import annotations

from abc import ABC, abstractmethod

from prince_gpt.core.enums import ActionName
from prince_gpt.core.schemas import ActionResult, GameState


class BasePrinceEnv(ABC):
    @abstractmethod
    def reset(self) -> GameState:
        raise NotImplementedError

    @abstractmethod
    def get_state(self) -> GameState:
        raise NotImplementedError

    @abstractmethod
    def step(self, action: ActionName) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def available_actions(self) -> list[ActionName]:
        raise NotImplementedError

    @abstractmethod
    def is_done(self) -> bool:
        raise NotImplementedError
