#!/usr/bin/env python3
"""scripts/generate-ui-tokens.py: the committed tables are current, the output is the same on every run, a stale table
is named by its token, and every source the generator promises to refuse is refused naming the token (D01 T14 §1)."""

import copy
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = ROOT / "scripts" / "generate-ui-tokens.py"
TOKENS = ROOT / "docs" / "design" / "tokens.json"
COMMITTED = ROOT / "native" / "ui" / "tokens"


class GenerateUiTokensTest(unittest.TestCase):
    def setUp(self):
        self.work = Path(tempfile.mkdtemp(prefix="ui-tokens-"))
        self.addCleanup(shutil.rmtree, self.work, ignore_errors=True)
        self.source = json.loads(TOKENS.read_text(encoding="utf-8"))

    def run_generator(self, *args, tokens=None):
        """(exit code, output) of the generator on a fixture (or the real tokens.json), writing under the work folder."""
        tokens_path = TOKENS
        if tokens is not None:
            tokens_path = self.work / "tokens.json"
            tokens_path.write_text(json.dumps(tokens), encoding="utf-8")
        proc = subprocess.run([sys.executable, "-B", str(SCRIPT), "--tokens", str(tokens_path), *args],
                              capture_output=True, text=True, timeout=120)
        return proc.returncode, proc.stdout + proc.stderr

    def color(self, tokens, name):
        return next(t for t in tokens["color"]["tokens"] if t["name"] == name)

    def refused(self, tokens, token_name):
        code, out = self.run_generator("--out", str(self.work / "out"), tokens=tokens)
        self.assertEqual(code, 2, out)
        self.assertIn(f"generate-ui-tokens: {token_name}:", out)
        self.assertFalse((self.work / "out").exists(), "a refused source wrote files")

    def test_the_committed_tables_are_current(self):
        code, out = self.run_generator("--check", "--out", str(COMMITTED))
        self.assertEqual(code, 0, out)
        self.assertIn("are current", out)

    def test_two_runs_write_the_same_bytes(self):
        first, second = self.work / "first", self.work / "second"
        for folder in (first, second):
            code, out = self.run_generator("--out", str(folder))
            self.assertEqual(code, 0, out)
        for name in ("tokens.generated.h", "tokens.generated.cpp"):
            self.assertEqual((first / name).read_bytes(), (second / name).read_bytes(), name)
            self.assertEqual((first / name).read_bytes(), (COMMITTED / name).read_bytes().replace(b"\r\n", b"\n"), name)
            head = (first / name).read_text(encoding="utf-8").splitlines()[:2]
            self.assertEqual(head, ["// generated from docs/design/tokens.json by scripts/generate-ui-tokens.py; do not edit",
                                    "// clang-format off"])

    def test_a_changed_value_is_stale_and_named(self):
        changed = copy.deepcopy(self.source)
        self.color(changed, "surface-panel")["value"]["dark"] = "#010203"
        next(t for t in changed["size"]["tokens"] if t["name"] == "titlebar-h")["value"] = "33px"
        code, out = self.run_generator("--check", "--out", str(COMMITTED), tokens=changed)
        self.assertEqual(code, 1, out)
        self.assertIn("stale: tokens.generated.cpp:", out)
        self.assertRegex(out, r"stale: tokens\.generated\.cpp:\d+: surface-panel \(dark\)")
        self.assertRegex(out, r"stale: tokens\.generated\.cpp:\d+: titlebar-h")
        self.assertNotIn("surface-panel (light)", out)
        self.assertIn("2 row(s) differ", out)

    def test_every_stale_row_is_named_however_many(self):
        """A change to every size token: each of them is named, with no cut-off."""
        changed = copy.deepcopy(self.source)
        names = []
        for group in ("spacing", "radius", "size"):
            for token in changed[group]["tokens"]:
                token["value"] = f"{float(token['value'][:-2]) + 1000}px"
                names.append(token["name"])
        self.assertGreater(len(names), 40)
        code, out = self.run_generator("--check", "--out", str(COMMITTED), tokens=changed)
        self.assertEqual(code, 1, out)
        named = re.findall(r"stale: tokens\.generated\.cpp:\d+: (\S+)", out)
        self.assertEqual(sorted(named), sorted(names))
        self.assertIn(f"{len(names)} row(s) differ", out)

    def test_a_missing_committed_file_is_stale(self):
        code, out = self.run_generator("--check", "--out", str(self.work / "nothing-here"))
        self.assertEqual(code, 1, out)

    def test_a_malformed_color_is_refused(self):
        for bad in ("#12345", "282828", "#gggggg", "rgb(1, 2, 3)", 7):
            tokens = copy.deepcopy(self.source)
            self.color(tokens, "frame")["value"]["medium"] = bad
            self.refused(tokens, "frame")

    def test_a_size_without_its_unit_is_refused(self):
        tokens = copy.deepcopy(self.source)
        next(t for t in tokens["size"]["tokens"] if t["name"] == "titlebar-h")["value"] = "32"
        self.refused(tokens, "titlebar-h")
        tokens = copy.deepcopy(self.source)
        tokens["type"]["groups"][0]["styles"][0]["lineHeight"] = "1.2"
        self.refused(tokens, tokens["type"]["groups"][0]["styles"][0]["name"])

    def test_an_alias_to_a_missing_token_is_refused(self):
        tokens = copy.deepcopy(self.source)
        self.color(tokens, "focus-ring")["value"] = "{state-outline}"
        self.refused(tokens, "focus-ring")
        tokens = copy.deepcopy(self.source)
        self.color(tokens, "focus-ring")["value"] = "{icon}"  # an alias of an alias has no value of its own
        self.refused(tokens, "focus-ring")

    def test_a_theme_without_a_value_is_refused(self):
        tokens = copy.deepcopy(self.source)
        del self.color(tokens, "divider")["value"]["light"]
        self.refused(tokens, "divider")
        tokens = copy.deepcopy(self.source)
        del tokens["shadow"]["tokens"][0]["value"]["darkest"]
        self.refused(tokens, tokens["shadow"]["tokens"][0]["name"])

    def test_a_name_used_twice_is_refused(self):
        tokens = copy.deepcopy(self.source)
        tokens["size"]["tokens"].append({"name": "frame", "value": "4px"})
        self.refused(tokens, "frame")
        tokens = copy.deepcopy(self.source)
        tokens["size"]["tokens"].append({"name": "control-h", "value": "4px"})  # collides with a generated neutral key
        self.refused(tokens, "control-h")
        tokens = copy.deepcopy(self.source)
        tokens["size"]["tokens"].append({"name": "space1", "value": "4px"})  # reads as space-1 without its hyphen
        self.refused(tokens, "space1")

    def test_an_incomplete_or_misnamed_high_contrast_mapping_is_refused(self):
        tokens = copy.deepcopy(self.source)
        del tokens["color"]["highContrast"]["tokens"]["scrim"]
        self.refused(tokens, "scrim")
        tokens = copy.deepcopy(self.source)
        tokens["color"]["highContrast"]["tokens"]["no-such-color"] = "window"
        self.refused(tokens, "no-such-color")
        tokens = copy.deepcopy(self.source)
        tokens["color"]["highContrast"]["tokens"]["frame"] = "COLOR_WINDOW"
        self.refused(tokens, "frame")
        tokens = copy.deepcopy(self.source)
        del tokens["color"]["highContrast"]
        self.refused(tokens, "color.highContrast")

    def test_an_unpaired_density_token_is_refused(self):
        tokens = copy.deepcopy(self.source)
        tokens["size"]["tokens"].append({"name": "gutter-compact", "value": "4px"})
        self.refused(tokens, "gutter-compact")

    def test_the_high_contrast_mapping_names_every_color_token_and_the_readme_rows(self):
        mapping = self.source["color"]["highContrast"]["tokens"]
        self.assertEqual(sorted(mapping), sorted(t["name"] for t in self.source["color"]["tokens"]))
        # The rows docs/design/README.md had before the mapping was written down, token by token.
        expected = {"frame": "window", "surface-panel": "window", "canvas-surround": "window",
                    "text-primary": "windowText", "text-secondary": "windowText", "icon": "windowText",
                    "border-control": "windowText", "divider": "windowText", "divider-strong": "windowText",
                    "text-disabled": "grayText", "state": "highlight", "state-subtle": "highlight",
                    "state-tint": "highlight", "state-on": "highlightText", "state-line": "highlight",
                    "focus-ring": "highlight", "state-text": "hotlight", "surface-control": "buttonFace",
                    "text-control": "buttonText"}
        for name, target in expected.items():
            self.assertEqual(mapping[name], target, name)


if __name__ == "__main__":
    unittest.main()
