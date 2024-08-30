import pytest

import json
from pathlib import Path

from abuild import parsers
from abuild.config import BuildStep


def describe_tox_parser():
    def test_should_see_tox_ini(tmp_path: Path):
        (tmp_path / 'tox.ini').write_text('[tox]')
        assert parsers.ToxParser().parse(tmp_path) == BuildStep(cmd='tox')

    def test_should_parse_pyproject_toml(tmp_path: Path):
        (tmp_path / 'pyproject.toml').write_text(
            '\n'.join(['[tool.tox]', 'legacy_tox_ini = """[tox]"""'])
        )
        assert parsers.ToxParser().parse(tmp_path) == BuildStep(cmd='tox')

    def test_should_parse_setup_cfg(tmp_path: Path):
        (tmp_path / 'setup.cfg').write_text(
            '\n'.join(
                [
                    '[tox:tox]',
                    'min_version = 4.0',
                    '',
                    '[testenv]',
                    'deps = pytest',
                ]
            )
        )
        assert parsers.ToxParser().parse(tmp_path) == BuildStep(cmd='tox')

    def test_should_not_return_on_empty_dir(tmp_path: Path):
        assert parsers.ToxParser().parse(tmp_path) is None


def describe_pyproject_parser():
    def test_should_parse_setuptools(tmp_path: Path):
        (tmp_path / 'pyproject.toml').write_text(
            '\n'.join(
                ['[build-system]', 'build-backend = "setuptools.build_meta"']
            )
        )
        assert parsers.PyProjectParser().parse(tmp_path) == BuildStep(
            cmd='python -m build'
        )

    def test_should_parse_flit(tmp_path: Path):
        (tmp_path / 'pyproject.toml').write_text(
            '\n'.join(
                ['[build-system]', 'build-backend = "flit_core.buildapi"']
            )
        )
        assert parsers.PyProjectParser().parse(tmp_path) == BuildStep(
            cmd='flit build'
        )

    def test_should_parse_poetry(tmp_path: Path):
        (tmp_path / 'pyproject.toml').write_text(
            '\n'.join(
                ['[build-system]', 'build-backend = "poetry.core.masonry.api"']
            )
        )
        assert parsers.PyProjectParser().parse(tmp_path) == BuildStep(
            cmd='poetry build'
        )

    def test_should_not_build_if_not_build_system_configured(tmp_path: Path):
        (tmp_path / 'pyproject.toml').write_text(
            '\n'.join(['[tool.poetry]', 'name = "some project"'])
        )
        assert parsers.PyProjectParser().parse(tmp_path) is None


def describe_package_json_parser():
    @pytest.fixture
    def with_package_json(tmp_path: Path):
        (tmp_path / 'package.json').write_text(
            json.dumps(
                {
                    'scripts': {
                        'test': 'some test command',
                        'build': 'some build command',
                    }
                }
            )
        )
        yield tmp_path

    def test_should_should_parse_target_section(with_package_json: Path):
        assert parsers.PackageJsonParser('test').parse(
            with_package_json
        ) == BuildStep(cmd='npm run test')

    def test_should_not_parse_if_section_not_present(with_package_json: Path):
        assert (
            parsers.PackageJsonParser('not exist').parse(with_package_json)
            is None
        )


def describe_docker_parser():
    def test_should_parse_with_docker(tmp_path: Path):
        (tmp_path / 'Dockerfile').write_text(
            '\n'.join(
                [
                    'FROM python3.9',
                    'RUN apt-get update && apt-get install htop',
                ]
            )
        )
        assert parsers.DockerParser().parse(tmp_path) == BuildStep(
            cmd='docker buildx build .'
        )

    def test_should_parse_single_docker_file(tmp_path: Path):
        (tmp_path / 'Dockerfile.service').write_text(
            '\n'.join(
                [
                    'FROM python3.9',
                    'RUN apt-get update && apt-get install htop',
                ]
            )
        )
        assert parsers.DockerParser().parse(tmp_path) == BuildStep(
            cmd='docker buildx build -F Dockerfile.service .'
        )

    def test_should_parse_dockerfile_and_other_docker_file(tmp_path: Path):
        (tmp_path / 'Dockerfile.service').write_text(
            '\n'.join(
                [
                    'FROM python3.9',
                    'RUN apt-get update && apt-get install htop',
                ]
            )
        )
        (tmp_path / 'Dockerfile').write_text(
            '\n'.join(
                [
                    'FROM python3.11',
                    'RUN apt-get update && apt-get install htop',
                ]
            )
        )
        assert parsers.DockerParser().parse(tmp_path) == BuildStep(
            cmd='docker buildx build -F Dockerfile .'
        )

    def test_should_skip_if_no_dockerfile(tmp_path: Path):
        assert parsers.DockerParser().parse(tmp_path) is None


def describe_makefile_parser():
    def test_should_parse_makefile(tmp_path: Path):
        (tmp_path / 'Makefile').write_text(
            '\n'.join(
                [
                    'test:',
                    '\t@echo "running tests"',
                    '',
                    'build:',
                    '\t@echo "building project"',
                ]
            )
        )
        assert parsers.MakefileParser().parse(tmp_path) == BuildStep(
            cmd='make'
        )

    def test_should_skip_if_no_makefile(tmp_path: Path):
        assert parsers.MakefileParser().parse(tmp_path) is None

    def test_should_not_parse_if_empty_makefile(tmp_path: Path):
        (tmp_path / 'Makefile').write_text('')
        assert parsers.MakefileParser().parse(tmp_path) is None
