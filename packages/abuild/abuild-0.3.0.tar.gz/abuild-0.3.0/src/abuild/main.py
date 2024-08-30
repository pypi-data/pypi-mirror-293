#!/usr/bin/env python
from io import StringIO
from pathlib import Path

import typer
import yaml

from . import parsers
from .build import build_component
from .config import Component, Config
from .state import state_update

app = typer.Typer()


@app.callback()
def main():
    # Set global options here
    pass


@app.command()
def build(
    tags: list[str] = typer.Option(
        [],
        '--tags',
        '-t',
        help='Only run certain tags',
    ),
    config: str = 'abuild.yaml',
):
    """Build components listed in the config file"""
    cfg = Config.from_file(Path(config))
    for component in cfg.components:
        with state_update(component.path, cfg.state_file) as need_rebuild:
            if need_rebuild:
                print(f'Building component: {component.display_name}')
                build_component(component, tags)


@app.command()
def parse():
    """Parse local directory and print a suggested configuration"""
    config = Config(components=[])
    for subdir in sorted(Path('.').iterdir()):
        if subdir.is_dir():
            steps = parsers.chain_of_command(
                subdir,
                parsers.ToxParser(),
                parsers.PyProjectParser(),
                parsers.DockerParser(),
                parsers.PackageJsonParser('test'),
                parsers.PackageJsonParser('build'),
            )
            if len(steps):
                config.components.append(
                    Component(path=str(subdir), steps=steps)
                )
    buf = StringIO()
    yaml.dump(config.model_dump(mode='json', exclude_unset=True), buf)
    print(buf.getvalue())


if __name__ == '__main__':
    app.run()
