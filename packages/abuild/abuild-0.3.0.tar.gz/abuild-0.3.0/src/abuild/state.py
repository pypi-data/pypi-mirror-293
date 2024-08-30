from typing import Iterator

import json
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field

from .hashing import hash_directory


class ComponentState(BaseModel):
    name: Path
    hash: str


class FullState(BaseModel):
    components: list[ComponentState] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def from_file(cls, filepath: Path):
        if not filepath.exists():
            return cls()
        with filepath.open('r') as f:
            return cls(**json.load(f))

    def to_file(self, filepath: Path):
        with filepath.open('w') as f:
            f.write(self.model_dump_json())


@contextmanager
def state_update(component: Path, state_file: Path) -> Iterator[bool]:
    state = FullState.from_file(state_file)
    idx = [i for i, c in enumerate(state.components) if c.name == component]
    current_hash = hash_directory(component)

    if len(idx) == 0:
        # not existing
        yield True
        FullState(
            components=state.components
            + [ComponentState(name=component, hash=current_hash)]
        ).to_file(state_file)
    else:
        full_component = state.components.pop(idx[0])
        if current_hash == full_component.hash:
            yield False
        else:
            yield True
            FullState(
                components=state.components
                + [ComponentState(name=component, hash=current_hash)]
            ).to_file(state_file)
