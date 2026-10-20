"""Validate portable Strategy files without executing their contents."""

from __future__ import annotations

import argparse
from pathlib import Path

from tools.focus_contract import parse_strategy


def validate_paths(paths: list[Path]) -> tuple[int, list[str]]:
    files: set[Path] = set()
    errors: list[str] = []
    for path in paths:
        if path.is_file():
            files.add(path.resolve())
        elif path.is_dir():
            found = list(path.rglob('STRATEGY.md'))
            files.update(file.resolve() for file in found)
            if not found:
                errors.append(f'{path}: no STRATEGY.md files found')
        else:
            errors.append(f'{path}: path does not exist')

    identities: dict[str, Path] = {}
    for path in sorted(files):
        try:
            package = parse_strategy(path.read_text(encoding='utf-8'))
        except (OSError, ValueError, RecursionError) as exc:
            errors.append(f'{path}: {exc}')
            continue
        identity = package.metadata.id
        if identity in identities:
            errors.append(f'{path}: duplicate id {identity!r} (also {identities[identity]})')
        else:
            identities[identity] = path
    return len(files), errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='*', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    paths = args.paths or [root / 'strategies', root / 'templates']
    count, errors = validate_paths(paths)
    for error in errors:
        print(f'ERROR: {error}')
    if errors:
        print(f'Validation failed: {len(errors)} error(s), {count} file(s).')
        return 1
    print(f'Validated {count} Strategy file(s).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
