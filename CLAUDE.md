# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`umake` is a small, dependency-free CLI tool that converts files between formats by shelling out to external tools (inkscape, pandoc, libreoffice, xelatex, heif-convert, ImageMagick's `convert`). The user names the *target* file (e.g. `umake file.pdf`) and umake finds a source file with the same stem and a convertible suffix in the same directory.

## Commands

```bash
uv run python -m pytest umake/tests/    # run tests
uv run python -m pytest umake/tests/test_converters.py::test_has_conversions   # single test
uv pip install .                        # install locally
umake --supports docx pdf               # smoke test (checks docx→pdf is supported)
```

Tests are pure unit tests on the converter registry; they do not invoke the external tools, so no converters need to be installed.

## Architecture

Two source files under `umake/`:

- `converters.py` — defines `registry`, a module-level dict mapping `(target_suffix, source_suffix)` tuples (with leading dots, e.g. `('.pdf', '.svg')`) to converter instances. **Note the key order: target first, source second.** Each converter is a `SubprocessConverter` subclass with a `_conversions` list and a `build_command(target, src)` method, registered at import time via the `@register_converter` class decorator.
- `main.py` — argument parsing and candidate resolution: given a target path, it scans the directory for files with the same stem whose suffix pairs with the target's in the registry, prompting the user interactively when multiple candidates exist or the target already exists (bypass with `--force`).

To add a new conversion: add a `(target_suffix, source_suffix)` pair to an existing converter's `_conversions`, or create a new `@register_converter` class in `converters.py`. Update the registry assertions in `umake/tests/test_converters.py` and the supported-transformations list in `README.md`.

`build/` and `dist/` contain stale build artifacts — never edit files there.

## Conventions

- Commit messages use short type prefixes: `ENH`, `MIN`, `BF`, etc.
- Version lives in `umake/umake_version.py` (read dynamically by `pyproject.toml`).
- No runtime Python dependencies; keep it that way (CI tests back to Python 3.10).
