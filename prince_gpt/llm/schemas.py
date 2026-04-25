from __future__ import annotations

from pydantic import BaseModel

from prince_gpt.core.enums import ActionName


class LLMActionChoice(BaseModel):
    action: ActionName
    rationale: str
