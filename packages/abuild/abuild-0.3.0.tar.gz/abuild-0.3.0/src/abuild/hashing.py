from typing import Iterable, cast

import fnmatch
from hashlib import md5
from pathlib import Path


def hash_directory(path: Path) -> str:

    h = md5()
    for filepath in sorted(all_files(path, [])):
        h.update(filepath.read_bytes())
    return h.hexdigest()


def all_files(
    root: Path, patterns: list[str] = cast(list[str], tuple)
) -> Iterable[Path]:
    ignore_file = root / '.abuildignore'
    if ignore_file.exists():
        patterns = list(
            set(patterns + ignore_file.read_text().splitlines(keepends=False))
        )
    else:
        patterns = list(set(patterns))

    for entry in root.glob('*'):
        if entry == ignore_file:
            continue
        elif matches(entry.name, [p.lstrip('/') for p in patterns]) or matches(
            entry, [f'*{p}' for p in patterns]
        ):
            continue

        if entry.is_dir():
            yield from all_files(entry, [p for p in patterns if p[0] != '/'])
        else:
            yield entry


def matches(entry: Path | str, patterns: list[str]) -> bool:
    for pattern in patterns:
        if fnmatch.fnmatch(str(entry), pattern):
            return True
    return False
