#!/usr/bin/env python3
"""Build dist/the-grill-pm-skill.zip. Standard library only."""
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "the-grill-pm-skill.zip"
TOP = "the-grill-pm"


def main():
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate.py")])
    if result.returncode != 0:
        print("validate.py failed; aborting build.")
        sys.exit(1)

    entries = [(ROOT / "skill" / "SKILL.md", "SKILL.md")]
    for folder in ("rubric", "prompts", "scenarios"):
        for path in sorted((ROOT / folder).rglob("*")):
            if path.is_file() and path.name != ".gitkeep" and "__pycache__" not in path.parts:
                entries.append((path, path.relative_to(ROOT).as_posix()))

    OUT.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for src, arc in entries:
            zf.write(src, f"{TOP}/{arc}")
    print(OUT)
    print(f"{OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
