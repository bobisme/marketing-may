#!/usr/bin/env python3
"""
Validate a JSON artifact against one of the skill's schemas.

Schemas (in assets/schemas/):
  - competitor_teardown.schema.json
  - event_taxonomy.schema.json
  - experiment_plan.schema.json
  - marketing_asset.schema.json
  - pricing_research.schema.json
  - evidence_ledger.schema.json

Usage:
  python validate_artifact.py path/to/artifact.json
    -> auto-detect schema from filename (e.g. *_evidence_ledger.json -> evidence_ledger)
  python validate_artifact.py artifact.json --schema evidence_ledger
  python validate_artifact.py artifact.json --schema-file path/to/custom.schema.json
  python validate_artifact.py artifact.json --strict   (treat all warnings as errors)

Requires: jsonschema (`pip install jsonschema`).
Falls back to a minimal best-effort validator if jsonschema is not installed —
the fallback only checks `required` and basic `type`, with a warning printed.

Exit codes:
  0  valid
  1  invalid (schema violations found)
  2  error (file not found, malformed JSON, schema not found)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "assets" / "schemas"
KNOWN_SCHEMAS = {
    "competitor_teardown": "competitor_teardown.schema.json",
    "event_taxonomy": "event_taxonomy.schema.json",
    "experiment_plan": "experiment_plan.schema.json",
    "marketing_asset": "marketing_asset.schema.json",
    "pricing_research": "pricing_research.schema.json",
    "evidence_ledger": "evidence_ledger.schema.json",
}


def detect_schema_from_filename(p: Path) -> Optional[str]:
    """Match the longest known-schema name appearing in the filename stem."""
    stem = p.stem.lower()
    matches = [name for name in KNOWN_SCHEMAS if name in stem]
    if not matches:
        return None
    return max(matches, key=len)


def load_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def fallback_validate(data: Any, schema: Dict[str, Any], path: str = "$") -> List[str]:
    """
    Minimal validator used when `jsonschema` isn't installed.
    Only checks `required` and basic `type` recursively. Issues are best-effort.
    """
    errors: List[str] = []

    def check(node: Any, sch: Dict[str, Any], cur: str) -> None:
        t = sch.get("type")
        if t == "object" and not isinstance(node, dict):
            errors.append(f"{cur}: expected object, got {type(node).__name__}")
            return
        if t == "array" and not isinstance(node, list):
            errors.append(f"{cur}: expected array, got {type(node).__name__}")
            return
        if t == "string" and not isinstance(node, str):
            errors.append(f"{cur}: expected string, got {type(node).__name__}")
            return
        if t == "number" and not isinstance(node, (int, float)):
            errors.append(f"{cur}: expected number, got {type(node).__name__}")
            return
        if t == "integer" and not isinstance(node, int):
            errors.append(f"{cur}: expected integer, got {type(node).__name__}")
            return

        if isinstance(node, dict):
            required = sch.get("required", [])
            for r in required:
                if r not in node:
                    errors.append(f"{cur}.{r}: required property missing")
            props = sch.get("properties", {})
            for k, v in node.items():
                if k in props:
                    check(v, props[k], f"{cur}.{k}")

        if isinstance(node, list):
            items = sch.get("items")
            if items:
                for i, v in enumerate(node):
                    check(v, items, f"{cur}[{i}]")

    check(data, schema, path)
    return errors


def validate_with_jsonschema(data: Any, schema: Dict[str, Any]) -> List[str]:
    """Use jsonschema if available; returns list of human-readable error strings."""
    try:
        from jsonschema import Draft202012Validator  # type: ignore
    except ImportError:
        return ["__no_jsonschema__"]
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
    out: List[str] = []
    for e in errors:
        path = "$" + "".join(f"[{p}]" if isinstance(p, int) else f".{p}" for p in e.absolute_path)
        out.append(f"{path}: {e.message}")
    return out


def main() -> int:
    p = argparse.ArgumentParser(description="Validate a JSON artifact against a skill schema.")
    p.add_argument("artifact", type=Path, nargs="?", help="JSON file to validate")
    p.add_argument("--schema", choices=sorted(KNOWN_SCHEMAS), help="schema name (overrides auto-detect)")
    p.add_argument("--schema-file", type=Path, help="path to a custom schema file")
    p.add_argument("--strict", action="store_true",
                   help="exit nonzero on any output, even from fallback validator")
    p.add_argument("--list-schemas", action="store_true", help="list known schemas and exit")
    args = p.parse_args()

    if args.list_schemas:
        for name, fname in sorted(KNOWN_SCHEMAS.items()):
            print(f"{name}: {fname}")
        return 0

    if args.artifact is None:
        p.error("artifact path is required (or use --list-schemas)")
    if not args.artifact.exists():
        print(f"Error: artifact not found: {args.artifact}", file=sys.stderr)
        return 2

    try:
        data = load_json(args.artifact)
    except json.JSONDecodeError as e:
        print(f"Error: malformed JSON in {args.artifact}: {e}", file=sys.stderr)
        return 2

    if args.schema_file:
        schema_path = args.schema_file
    else:
        schema_name = args.schema or detect_schema_from_filename(args.artifact)
        if not schema_name:
            print(f"Error: cannot detect schema from filename {args.artifact.name!r}; "
                  f"specify --schema or --schema-file. Known: {', '.join(sorted(KNOWN_SCHEMAS))}",
                  file=sys.stderr)
            return 2
        schema_path = SCHEMAS_DIR / KNOWN_SCHEMAS[schema_name]

    if not schema_path.exists():
        print(f"Error: schema file not found: {schema_path}", file=sys.stderr)
        return 2

    try:
        schema = load_json(schema_path)
    except json.JSONDecodeError as e:
        print(f"Error: malformed schema {schema_path}: {e}", file=sys.stderr)
        return 2

    errors = validate_with_jsonschema(data, schema)
    used_fallback = errors == ["__no_jsonschema__"]
    if used_fallback:
        print("Note: jsonschema not installed; using fallback validator (only checks required + type). "
              "`pip install jsonschema` for full validation.", file=sys.stderr)
        errors = fallback_validate(data, schema)

    if not errors:
        print(f"OK — {args.artifact} validates against {schema_path.name}")
        return 0

    print(f"INVALID — {len(errors)} error(s) against {schema_path.name}:")
    for e in errors:
        print(f"  {e}")
    return 1 if (errors and not used_fallback) or args.strict else (1 if errors else 0)


if __name__ == "__main__":
    raise SystemExit(main())
