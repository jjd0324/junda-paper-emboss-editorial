#!/usr/bin/env python3
"""Validate the distributable structure of this skill project without dependencies."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_RELATIVE = Path("skills/junda-paper-emboss-editorial")
EXPECTED_NAME = "junda-paper-emboss-editorial"
REQUIRED_FILES = (
    Path("README.md"),
    Path("LICENSE"),
    Path("ASSETS-LICENSE"),
    Path(".github/workflows/validate.yml"),
    Path("evals/public/README.md"),
    Path("evals/public/behavior-cases.jsonl"),
    Path("evals/public/visual-rubric.md"),
    SKILL_RELATIVE / "SKILL.md",
    SKILL_RELATIVE / "agents/openai.yaml",
    SKILL_RELATIVE / "references/design-system.md",
    SKILL_RELATIVE / "references/prompt-blueprint.md",
    SKILL_RELATIVE / "references/reference-image-workflow.md",
    SKILL_RELATIVE / "references/strict-text-mode.md",
    SKILL_RELATIVE / "assets/editable-text-overlay-3x4.svg",
    SKILL_RELATIVE / "assets/template-previews/manifest.json",
)
FORBIDDEN_TEXT = (
    "OPENAI" + "_API_KEY=",
    "gh" + "p_",
    "github_" + "pat_",
    "BEGIN " + "PRIVATE KEY",
)
LOCAL_LINK = re.compile(r"\]\(([^)#]+)(?:#[^)]+)?\)")
PREVIEW_LICENSE = "CC-BY-4.0"
PREVIEW_COPYRIGHT_HOLDER = "Junda (俊达)"
PREVIEW_PROVENANCE_KIND = "project-generated-ai-concept-preview"
PREVIEW_GENERATOR = "OpenAI Media Service"
TEXT_OVERLAY_RELATIVE = SKILL_RELATIVE / "assets/editable-text-overlay-3x4.svg"
TEXT_OVERLAY_PLACEHOLDERS = ("{{TITLE}}", "{{SUBTITLE}}", "{{INDEX}}")


def read_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.+)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip('"')
    return values


def png_dimensions(path: Path) -> tuple[int, int] | None:
    payload = path.read_bytes()
    if len(payload) < 24 or payload[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if payload[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", payload[16:24])


def check_local_links(root: Path) -> list[str]:
    errors: list[str] = []
    root_resolved = root.resolve()
    for markdown_path in root.rglob("*.md"):
        text = markdown_path.read_text(encoding="utf-8")
        for href in LOCAL_LINK.findall(text):
            if re.match(r"^[a-z]+:", href, flags=re.IGNORECASE):
                continue
            target = (markdown_path.parent / href).resolve()
            if not target.is_relative_to(root_resolved):
                errors.append(f"link escapes project: {markdown_path.relative_to(root)} -> {href}")
            elif not target.exists():
                errors.append(f"broken link: {markdown_path.relative_to(root)} -> {href}")
    return errors


def check_manifest(root: Path) -> list[str]:
    errors: list[str] = []
    asset_dir = root / SKILL_RELATIVE / "assets/template-previews"
    manifest_path = asset_dir / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid preview manifest: {exc}"]
    items = manifest.get("items")
    if not isinstance(items, list) or len(items) < 2:
        return ["preview manifest must declare at least two items"]
    ids: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            errors.append("preview item is not an object")
            continue
        item_id = item.get("id")
        preview = item.get("preview")
        if not isinstance(item_id, str) or item_id in ids:
            errors.append("preview IDs must be unique strings")
        else:
            ids.add(item_id)
        if not isinstance(preview, str):
            errors.append(f"preview {item_id!r} has no file")
            continue
        image_path = asset_dir / preview
        dimensions = png_dimensions(image_path) if image_path.is_file() else None
        if dimensions is None or min(dimensions) < 256:
            errors.append(f"preview is not a valid usable PNG: {preview}")
        for key in ("ratio", "mode", "checks"):
            if key not in item:
                errors.append(f"preview {preview} missing {key}")

        if item.get("license") != PREVIEW_LICENSE:
            errors.append(f"preview {preview} must declare {PREVIEW_LICENSE}")
        if item.get("copyright_holder") != PREVIEW_COPYRIGHT_HOLDER:
            errors.append(f"preview {preview} must declare its copyright holder")

        provenance = item.get("provenance")
        if not isinstance(provenance, dict):
            errors.append(f"preview {preview} missing provenance")
        else:
            if provenance.get("kind") != PREVIEW_PROVENANCE_KIND:
                errors.append(f"preview {preview} has an invalid provenance kind")
            if provenance.get("generator") != PREVIEW_GENERATOR:
                errors.append(f"preview {preview} has an invalid provenance generator")
            if not isinstance(provenance.get("source_material"), str):
                errors.append(f"preview {preview} needs a provenance source_material")

        expected_hash = item.get("sha256")
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            errors.append(f"preview {preview} has an invalid sha256")
        elif image_path.is_file():
            actual_hash = hashlib.sha256(image_path.read_bytes()).hexdigest()
            if actual_hash != expected_hash:
                errors.append(f"preview hash mismatch: {preview}")
    return errors


def check_behavior_cases(root: Path) -> list[str]:
    path = root / "evals/public/behavior-cases.jsonl"
    errors: list[str] = []
    ids: set[str] = set()
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(lines) < 6:
        return ["need at least six public behavior cases"]
    for line_number, line in enumerate(lines, start=1):
        try:
            case = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid behavior case JSON at line {line_number}: {exc.msg}")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or case_id in ids:
            errors.append(f"behavior case line {line_number} has a missing or duplicate id")
        else:
            ids.add(case_id)
        for key in ("request", "must", "must_not"):
            if key not in case or not case[key]:
                errors.append(f"behavior case {case_id!r} missing {key}")
    return errors


def check_text_overlay_template(root: Path) -> list[str]:
    path = root / TEXT_OVERLAY_RELATIVE
    errors: list[str] = []
    try:
        ET.parse(path)
    except (OSError, ET.ParseError) as exc:
        return [f"invalid editable text overlay SVG: {exc}"]
    contents = path.read_text(encoding="utf-8")
    for placeholder in TEXT_OVERLAY_PLACEHOLDERS:
        if placeholder not in contents:
            errors.append(f"editable text overlay missing {placeholder}")
    return errors


def validate(root: Path = PROJECT_ROOT) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    for relative_path in REQUIRED_FILES:
        if not (root / relative_path).is_file():
            errors.append(f"missing required file: {relative_path}")

    if errors:
        return errors

    skill_file = root / SKILL_RELATIVE / "SKILL.md"
    frontmatter = read_frontmatter(skill_file)
    if frontmatter.get("name") != EXPECTED_NAME:
        errors.append(f"SKILL.md name must be {EXPECTED_NAME}")
    if not frontmatter.get("description") or "TODO" in frontmatter["description"]:
        errors.append("SKILL.md needs a concrete description")

    openai_yaml = (root / SKILL_RELATIVE / "agents/openai.yaml").read_text(encoding="utf-8")
    if f"${EXPECTED_NAME}" not in openai_yaml:
        errors.append("openai.yaml default prompt must invoke the current skill name")
    if "[TODO" in skill_file.read_text(encoding="utf-8"):
        errors.append("SKILL.md contains an unfinished placeholder")

    errors.extend(check_local_links(root))
    errors.extend(check_manifest(root))
    errors.extend(check_behavior_cases(root))
    errors.extend(check_text_overlay_template(root))

    for text_path in root.rglob("*"):
        if not text_path.is_file() or text_path.suffix.lower() not in {".md", ".yaml", ".yml", ".json", ".py"}:
            continue
        contents = text_path.read_text(encoding="utf-8")
        for marker in FORBIDDEN_TEXT:
            if marker in contents:
                errors.append(f"forbidden sensitive marker in {text_path.relative_to(root)}")
    gitignore = root / ".gitignore"
    gitignore_lines = gitignore.read_text(encoding="utf-8").splitlines()
    required_ignores = (".DS_Store", ".env", ".env.*", "!.env.example")
    for entry in required_ignores:
        if entry not in gitignore_lines:
            errors.append(f".gitignore must contain {entry}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT)
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Project validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
