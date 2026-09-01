"""Load guide specs from YAML or JSON, with errors that point at the file."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Guide

try:  # pragma: no cover - exercised by environment, not by tests
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


class GuideLoadError(Exception):
    """Raised when a guide file cannot be read or does not satisfy the schema."""


def load_guide(path: str | Path) -> Guide:
    path = Path(path)
    if not path.exists():
        raise GuideLoadError(f"{path}: no such file")
    raw = path.read_text(encoding="utf-8")
    data = _parse(raw, path)
    try:
        return Guide.from_dict(data)
    except ValueError as exc:
        raise GuideLoadError(f"{path}: {exc}") from exc


def load_guides(paths: list[str | Path]) -> list[Guide]:
    return [load_guide(p) for p in paths]


def discover(directory: str | Path) -> list[Path]:
    """Every guide spec under `directory`, in stable order."""
    directory = Path(directory)
    if not directory.is_dir():
        raise GuideLoadError(f"{directory}: not a directory")
    found = [
        p for p in sorted(directory.rglob("*"))
        if p.suffix.lower() in {".yaml", ".yml", ".json"} and p.is_file()
    ]
    return found


def _parse(raw: str, path: Path) -> Any:
    if path.suffix.lower() == ".json":
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise GuideLoadError(f"{path}: invalid JSON: {exc}") from exc
    if yaml is None:
        raise GuideLoadError(
            f"{path}: PyYAML is not installed; install it or use a .json guide spec"
        )
    try:
        return yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise GuideLoadError(f"{path}: invalid YAML: {exc}") from exc
