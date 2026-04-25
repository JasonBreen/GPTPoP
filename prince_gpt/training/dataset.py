from __future__ import annotations

from prince_gpt.core.schemas import TransitionRecord


class TransitionDataset:
    """Simple in-memory dataset placeholder for future training."""

    def __init__(self, records: list[TransitionRecord] | None = None) -> None:
        self.records = records or []

    def __len__(self) -> int:
        return len(self.records)
