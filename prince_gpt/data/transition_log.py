from __future__ import annotations

import json
from pathlib import Path

from prince_gpt.core.schemas import TransitionRecord


class TransitionLogger:
    def __init__(self) -> None:
        self.records: list[TransitionRecord] = []

    def append(self, record: TransitionRecord) -> None:
        self.records.append(record)

    def save_jsonl(self, path: str | Path) -> None:
        output_path = Path(path)
        with output_path.open("w", encoding="utf-8") as f:
            for record in self.records:
                f.write(json.dumps(record.model_dump(mode="json")) + "\n")

    @classmethod
    def load_jsonl(cls, path: str | Path) -> "TransitionLogger":
        logger = cls()
        input_path = Path(path)
        with input_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                logger.records.append(TransitionRecord.model_validate_json(line))
        return logger
