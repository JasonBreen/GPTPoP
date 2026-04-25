# prince-gpt

`prince-gpt` is a Python software harness for building an AI agent that can play classic Prince of Persia.

## Project goal

Build a clean, testable, modular foundation for:

- structured game state modeling,
- macro-action execution,
- deterministic planning,
- transition logging for later dataset generation,
- and future training/inference adapters.

This repository deliberately starts **without** real game integration and **without** model training.

## Current milestone

Implemented in this milestone:

- a mock Prince of Persia environment,
- tile-based room/hazard representation,
- macro-actions,
- a simple A* planner over simulated actions,
- transition logging with JSONL I/O,
- and tests validating route finding across a gap.

## Future milestones

1. SDLPoP instrumentation adapter.
2. Real macro-action timing.
3. Transition dataset collection.
4. Imitation learning policy.
5. MaskablePPO training.
6. Local LLM plan-repair adapter.

## Quickstart

```bash
python -m venv .venv
pip install -e ".[dev]"
pytest
```
