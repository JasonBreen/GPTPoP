from __future__ import annotations

from prince_gpt.core.schemas import ActionResult


class ActionVerifier:
    """Placeholder verifier for future frame-level validation."""

    def verify(self, result: ActionResult) -> bool:
        return result.success
