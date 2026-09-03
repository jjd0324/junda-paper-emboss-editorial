from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
from validate_project import validate  # noqa: E402


class ValidateProjectTests(unittest.TestCase):
    def test_current_project_is_valid(self) -> None:
        self.assertEqual(validate(PROJECT_ROOT), [])

    def test_missing_reference_workflow_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            clone = Path(temp_dir) / "project"
            shutil.copytree(PROJECT_ROOT, clone)
            (clone / "skills/junda-paper-emboss-editorial/references/reference-image-workflow.md").unlink()
            errors = validate(clone)
            self.assertTrue(any("reference-image-workflow.md" in error for error in errors))

    def test_default_prompt_must_use_current_slug(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            clone = Path(temp_dir) / "project"
            shutil.copytree(PROJECT_ROOT, clone)
            metadata = clone / "skills/junda-paper-emboss-editorial/agents/openai.yaml"
            metadata.write_text(metadata.read_text(encoding="utf-8").replace("$junda-paper-emboss-editorial", "$old-name"), encoding="utf-8")
            errors = validate(clone)
            self.assertIn("openai.yaml default prompt must invoke the current skill name", errors)

    def test_env_files_must_be_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            clone = Path(temp_dir) / "project"
            shutil.copytree(PROJECT_ROOT, clone)
            gitignore = clone / ".gitignore"
            gitignore.write_text(
                gitignore.read_text(encoding="utf-8").replace(".env\n", ""),
                encoding="utf-8",
            )
            errors = validate(clone)
            self.assertIn(".gitignore must contain .env", errors)

    def test_preview_hash_tampering_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            clone = Path(temp_dir) / "project"
            shutil.copytree(PROJECT_ROOT, clone)
            preview = clone / "skills/junda-paper-emboss-editorial/assets/template-previews/01-pause-deboss-poster.png"
            payload = bytearray(preview.read_bytes())
            payload[-1] ^= 1
            preview.write_bytes(payload)
            errors = validate(clone)
            self.assertIn("preview hash mismatch: 01-pause-deboss-poster.png", errors)

    def test_editable_text_overlay_requires_title_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            clone = Path(temp_dir) / "project"
            shutil.copytree(PROJECT_ROOT, clone)
            template = clone / "skills/junda-paper-emboss-editorial/assets/editable-text-overlay-3x4.svg"
            template.write_text(
                template.read_text(encoding="utf-8").replace("{{TITLE}}", ""),
                encoding="utf-8",
            )
            errors = validate(clone)
            self.assertIn("editable text overlay missing {{TITLE}}", errors)
