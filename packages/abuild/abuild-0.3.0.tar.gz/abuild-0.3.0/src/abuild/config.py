from pathlib import Path

import yaml
from pydantic import BaseModel


class BuildStep(BaseModel):
    name: str | None = None
    cmd: str
    break_on_error: bool = True
    tag: str = ':notag:'

    @property
    def display_name(self) -> str:
        if self.name:
            return self.name
        else:
            return self.cmd


class Component(BaseModel):
    name: str | None = None
    path: Path
    steps: list[BuildStep]

    @property
    def display_name(self) -> str:
        if self.name:
            return self.name
        else:
            return str(self.path)


class Config(BaseModel):
    components: list[Component]
    state_file: Path = Path('.abuild_state')

    @classmethod
    def from_file(cls, path: Path):
        with path.open('r') as f:
            return cls(**yaml.safe_load(f))
