# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0,<7"]
# ///
"""The `validate` check for comeni-code-content (Comeni Code, M0 part 9 spec).

Until the node format exists (Comeni Code M1), it checks only what already has rules: the licence
and README are present, every YAML file parses, and no file is larger than 5 MB.
Run from the repository root: uv run .github/scripts/validate.py
"""

import subprocess
import sys
from pathlib import Path

import yaml

MAX_BYTES = 5 * 1024 * 1024
LICENCE_FIRST_LINE = "Attribution 4.0 International"


def tracked_files() -> list[Path]:
    out = subprocess.run(["git", "ls-files", "-z"], capture_output=True, check=True).stdout
    return [Path(name) for name in out.decode().split("\0") if name]


def problems(files: list[Path]) -> list[str]:
    found: list[str] = []
    licence = Path("LICENSE")
    if not licence.is_file():
        found.append("LICENSE is missing")
    elif licence.read_text(encoding="utf-8").splitlines()[:1] != [LICENCE_FIRST_LINE]:
        found.append(f"LICENSE does not start with {LICENCE_FIRST_LINE!r} (CC BY 4.0)")
    if not Path("README.md").is_file():
        found.append("README.md is missing")
    for path in files:
        if not path.is_file():
            continue
        if path.stat().st_size > MAX_BYTES:
            found.append(f"{path} is larger than 5 MB")
        if path.suffix in {".yaml", ".yml"}:
            try:
                yaml.safe_load(path.read_text(encoding="utf-8"))
            except yaml.YAMLError as error:
                mark = getattr(error, "problem_mark", None)
                where = f":{mark.line + 1}" if mark is not None else ""
                what = getattr(error, "problem", None) or "does not parse"
                found.append(f"{path}{where}: not valid YAML ({what})")
    return found


def main() -> int:
    files = tracked_files()
    found = problems(files)
    for problem in found:
        print(f"FAIL: {problem}")
    if found:
        return 1
    print(f"ok: licence, README, YAML and sizes across {len(files)} files")
    print("Node validation arrives with Comeni Code M1; this check does not validate nodes yet.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
