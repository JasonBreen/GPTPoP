from __future__ import annotations

from prince_gpt.core.enums import ActionName


def all_actions() -> list[ActionName]:
    return list(ActionName)
