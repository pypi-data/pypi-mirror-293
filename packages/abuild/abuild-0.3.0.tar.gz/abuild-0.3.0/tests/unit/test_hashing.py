import pytest

from typing import Iterable

from pathlib import Path

from abuild import hashing


def describe_all_files():
    def should_list_all_files_if_no_ignore(tmp_path: Path):
        (tmp_path / 'a_file.txt').write_text('a')
        (tmp_path / 'b_file.txt').write_text('b')
        assert as_sorted_list(hashing.all_files(tmp_path, [])) == [
            f'{str(tmp_path)}/a_file.txt',
            f'{str(tmp_path)}/b_file.txt',
        ]

    @pytest.fixture
    def populated_dir(tmp_path: Path):
        (tmp_path / 'a_file.txt').write_text('a_file')
        (tmp_path / 'another_file.txt').write_text('another_file')
        (tmp_path / '.abuildignore').write_text('another_*')
        yield tmp_path

    def should_drop_files_that_match_ignore(populated_dir: Path):
        assert as_sorted_list(hashing.all_files(populated_dir, [])) == [
            f'{str(populated_dir)}/a_file.txt',
        ]

    @pytest.fixture
    def complex_dir(tmp_path: Path) -> Path:
        (tmp_path / 'file1.txt').write_text('1')
        (tmp_path / 'file2.txt').write_text('2')
        (tmp_path / 'file3.txt').write_text('3')
        (tmp_path / 'subdir1').mkdir()
        (tmp_path / 'subdir2').mkdir()
        (tmp_path / 'subdir3').mkdir()
        subdir1 = tmp_path / 'subdir1'
        subdir2 = tmp_path / 'subdir2'
        subdir3 = tmp_path / 'subdir3'
        (subdir1 / 'file1.txt').write_text('11')
        (subdir1 / 'file2.txt').write_text('12')
        (subdir1 / 'file3.txt').write_text('13')
        (subdir2 / 'file1.txt').write_text('21')
        (subdir2 / 'file2.txt').write_text('22')
        (subdir2 / 'file3.txt').write_text('23')
        (subdir3 / 'file1.txt').write_text('31')
        (subdir3 / 'file2.txt').write_text('32')
        (subdir3 / 'file3.txt').write_text('33')
        subsubdir11 = subdir1 / 'subsubdir11'
        subsubdir11.mkdir()
        (subsubdir11 / 'file1.txt').write_text('111')
        (subsubdir11 / 'file2.txt').write_text('112')

        yield tmp_path

    def should_work_on_complex_nested_directories(complex_dir: Path):
        assert as_sorted_list(hashing.all_files(complex_dir, [])) == [
            f'{str(complex_dir)}/file1.txt',
            f'{str(complex_dir)}/file2.txt',
            f'{str(complex_dir)}/file3.txt',
            f'{str(complex_dir)}/subdir1/file1.txt',
            f'{str(complex_dir)}/subdir1/file2.txt',
            f'{str(complex_dir)}/subdir1/file3.txt',
            f'{str(complex_dir)}/subdir1/subsubdir11/file1.txt',
            f'{str(complex_dir)}/subdir1/subsubdir11/file2.txt',
            f'{str(complex_dir)}/subdir2/file1.txt',
            f'{str(complex_dir)}/subdir2/file2.txt',
            f'{str(complex_dir)}/subdir2/file3.txt',
            f'{str(complex_dir)}/subdir3/file1.txt',
            f'{str(complex_dir)}/subdir3/file2.txt',
            f'{str(complex_dir)}/subdir3/file3.txt',
        ]

    def should_ignore_local_files_if_prefixed_with_slash(complex_dir: Path):
        (complex_dir / '.abuildignore').write_text('/file1.txt')

        assert as_sorted_list(hashing.all_files(complex_dir, [])) == [
            f'{str(complex_dir)}/file2.txt',
            f'{str(complex_dir)}/file3.txt',
            f'{str(complex_dir)}/subdir1/file1.txt',
            f'{str(complex_dir)}/subdir1/file2.txt',
            f'{str(complex_dir)}/subdir1/file3.txt',
            f'{str(complex_dir)}/subdir1/subsubdir11/file1.txt',
            f'{str(complex_dir)}/subdir1/subsubdir11/file2.txt',
            f'{str(complex_dir)}/subdir2/file1.txt',
            f'{str(complex_dir)}/subdir2/file2.txt',
            f'{str(complex_dir)}/subdir2/file3.txt',
            f'{str(complex_dir)}/subdir3/file1.txt',
            f'{str(complex_dir)}/subdir3/file2.txt',
            f'{str(complex_dir)}/subdir3/file3.txt',
        ]

    def should_ignore_file_through_hierarchy_if_no_slash_prefix(
        complex_dir: Path,
    ):
        (complex_dir / '.abuildignore').write_text('file1.txt')

        assert as_sorted_list(hashing.all_files(complex_dir, [])) == [
            f'{str(complex_dir)}/file2.txt',
            f'{str(complex_dir)}/file3.txt',
            f'{str(complex_dir)}/subdir1/file2.txt',
            f'{str(complex_dir)}/subdir1/file3.txt',
            f'{str(complex_dir)}/subdir1/subsubdir11/file2.txt',
            f'{str(complex_dir)}/subdir2/file2.txt',
            f'{str(complex_dir)}/subdir2/file3.txt',
            f'{str(complex_dir)}/subdir3/file2.txt',
            f'{str(complex_dir)}/subdir3/file3.txt',
        ]

    def should_apply_ignore_only_to_subdirs(complex_dir: Path):
        (complex_dir / 'subdir1' / '.abuildignore').write_text('file1.txt')
        assert as_sorted_list(hashing.all_files(complex_dir, [])) == [
            f'{str(complex_dir)}/file1.txt',
            f'{str(complex_dir)}/file2.txt',
            f'{str(complex_dir)}/file3.txt',
            f'{str(complex_dir)}/subdir1/file2.txt',
            f'{str(complex_dir)}/subdir1/file3.txt',
            f'{str(complex_dir)}/subdir1/subsubdir11/file2.txt',
            f'{str(complex_dir)}/subdir2/file1.txt',
            f'{str(complex_dir)}/subdir2/file2.txt',
            f'{str(complex_dir)}/subdir2/file3.txt',
            f'{str(complex_dir)}/subdir3/file1.txt',
            f'{str(complex_dir)}/subdir3/file2.txt',
            f'{str(complex_dir)}/subdir3/file3.txt',
        ]

    def should_work_with_directory_names(complex_dir: Path):
        (complex_dir / '.abuildignore').write_text('subdir1')
        assert as_sorted_list(hashing.all_files(complex_dir, [])) == [
            f'{str(complex_dir)}/file1.txt',
            f'{str(complex_dir)}/file2.txt',
            f'{str(complex_dir)}/file3.txt',
            f'{str(complex_dir)}/subdir2/file1.txt',
            f'{str(complex_dir)}/subdir2/file2.txt',
            f'{str(complex_dir)}/subdir2/file3.txt',
            f'{str(complex_dir)}/subdir3/file1.txt',
            f'{str(complex_dir)}/subdir3/file2.txt',
            f'{str(complex_dir)}/subdir3/file3.txt',
        ]

    def should_work_with_directory_names_further_down(complex_dir: Path):
        (complex_dir / '.abuildignore').write_text('subsubdir11')
        assert as_sorted_list(hashing.all_files(complex_dir, [])) == [
            f'{str(complex_dir)}/file1.txt',
            f'{str(complex_dir)}/file2.txt',
            f'{str(complex_dir)}/file3.txt',
            f'{str(complex_dir)}/subdir1/file1.txt',
            f'{str(complex_dir)}/subdir1/file2.txt',
            f'{str(complex_dir)}/subdir1/file3.txt',
            f'{str(complex_dir)}/subdir2/file1.txt',
            f'{str(complex_dir)}/subdir2/file2.txt',
            f'{str(complex_dir)}/subdir2/file3.txt',
            f'{str(complex_dir)}/subdir3/file1.txt',
            f'{str(complex_dir)}/subdir3/file2.txt',
            f'{str(complex_dir)}/subdir3/file3.txt',
        ]

    def should_work_with_glob_patterns(complex_dir: Path):
        (complex_dir / '.abuildignore').write_text('*1.txt')
        assert as_sorted_list(hashing.all_files(complex_dir, [])) == [
            f'{str(complex_dir)}/file2.txt',
            f'{str(complex_dir)}/file3.txt',
            f'{str(complex_dir)}/subdir1/file2.txt',
            f'{str(complex_dir)}/subdir1/file3.txt',
            f'{str(complex_dir)}/subdir1/subsubdir11/file2.txt',
            f'{str(complex_dir)}/subdir2/file2.txt',
            f'{str(complex_dir)}/subdir2/file3.txt',
            f'{str(complex_dir)}/subdir3/file2.txt',
            f'{str(complex_dir)}/subdir3/file3.txt',
        ]

    def should_work_with_multiple_patterns(complex_dir: Path):
        (complex_dir / '.abuildignore').write_text('file1*\nsubdir1')
        assert as_sorted_list(hashing.all_files(complex_dir, [])) == [
            f'{str(complex_dir)}/file2.txt',
            f'{str(complex_dir)}/file3.txt',
            f'{str(complex_dir)}/subdir2/file2.txt',
            f'{str(complex_dir)}/subdir2/file3.txt',
            f'{str(complex_dir)}/subdir3/file2.txt',
            f'{str(complex_dir)}/subdir3/file3.txt',
        ]

    def should_aggregate_patterns_through_hierarchy(complex_dir: Path):
        (complex_dir / '.abuildignore').write_text('file1*')
        (complex_dir / 'subdir1' / '.abuildignore').write_text('file2.txt')
        assert as_sorted_list(hashing.all_files(complex_dir, [])) == [
            f'{str(complex_dir)}/file2.txt',
            f'{str(complex_dir)}/file3.txt',
            f'{str(complex_dir)}/subdir1/file3.txt',
            f'{str(complex_dir)}/subdir2/file2.txt',
            f'{str(complex_dir)}/subdir2/file3.txt',
            f'{str(complex_dir)}/subdir3/file2.txt',
            f'{str(complex_dir)}/subdir3/file3.txt',
        ]


def as_sorted_list(it: Iterable[Path]) -> list[str]:
    return list(map(str, sorted(it)))
