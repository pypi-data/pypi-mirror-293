from abc import ABC, abstractmethod

import configparser
import json
import tomllib
from pathlib import Path

from .config import BuildStep


class ParserInterface(ABC):
    @abstractmethod
    def parse(self, project_root: Path) -> BuildStep | None:
        pass


def chain_of_command(
    project_root: Path, *parsers: ParserInterface
) -> list[BuildStep]:
    all_build_steps = (parser.parse(project_root) for parser in parsers)
    return [s for s in all_build_steps if s is not None]  # type: ignore


class ToxParser(ParserInterface):
    def parse(self, project_root: Path) -> BuildStep | None:
        tox_ini = project_root / 'tox.ini'
        if tox_ini.exists():
            return BuildStep(cmd='tox')

        pyproject_toml = project_root / 'pyproject.toml'
        if pyproject_toml.exists():
            config = tomllib.loads(pyproject_toml.read_text())
            if config['tool']['tox']['legacy_tox_ini']:
                return BuildStep(cmd='tox')

        setup_cfg = project_root / 'setup.cfg'
        if setup_cfg.exists():
            parser = configparser.ConfigParser()
            parser.read([str(setup_cfg)])
            print(parser)
            if parser.has_section('tox:tox'):
                return BuildStep(cmd='tox')

        return None


class PyProjectParser(ParserInterface):
    def parse(self, project_root: Path) -> BuildStep | None:
        pyproject_toml = project_root / 'pyproject.toml'
        if pyproject_toml.exists():
            config = tomllib.loads(pyproject_toml.read_text())
            build_backend = config.get('build-system', {}).get('build-backend')
            if not build_backend:
                return None

            if build_backend == 'setuptools.build_meta':
                return BuildStep(cmd='python -m build')
            elif build_backend in ['flit.buildapi', 'flit_core.buildapi']:
                # NOTE: flit could also do upload
                return BuildStep(cmd='flit build')
            elif build_backend == 'poetry.core.masonry.api':
                return BuildStep(cmd='poetry build')

        return None


class PackageJsonParser(ParserInterface):
    section: str

    def __init__(self, section: str):
        self.section = section

    def parse(self, project_root: Path) -> BuildStep | None:
        package_json = project_root / 'package.json'
        if package_json.exists():
            config = json.loads(package_json.read_text())
            if config['scripts'].get(self.section):
                return BuildStep(cmd=f'npm run {self.section}')
        return None


class DockerParser(ParserInterface):
    def parse(self, project_root: Path) -> BuildStep | None:
        dockerfile = project_root / 'Dockerfile'
        dockerfiles = list(project_root.glob('Dockerfile*'))
        if dockerfile.exists():
            if len(dockerfiles) == 1:
                return BuildStep(cmd='docker buildx build .')
            else:
                return BuildStep(cmd='docker buildx build -F Dockerfile .')
        elif len(dockerfiles) == 1:
            return BuildStep(
                cmd=f'docker buildx build -F {dockerfiles[0].name} .'
            )

        return None


class MakefileParser(ParserInterface):
    def parse(self, project_root: Path) -> BuildStep | None:
        makefile = project_root / 'Makefile'
        if self._not_empty(makefile):
            return BuildStep(cmd='make')
        return None

    @staticmethod
    def _not_empty(file: Path) -> bool:
        return file.exists() and file.stat().st_size > 0
