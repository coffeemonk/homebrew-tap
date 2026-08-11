#!/usr/bin/env python3
"""
Updates a Homebrew formula file with new version and sha256 checksums.

Usage:
    python3 update_formula.py <formula_path> <version> <arm64_sha256> <intel_sha256>
"""

import re
import sys


def update_formula(path: str, version: str, arm_sha: str, intel_sha: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update formula version
    content = re.sub(r'version ".*?"', f'version "{version}"', content, count=1)

    # Replace sha256 checksums (arm64 first, then intel x64)
    shas = [arm_sha, intel_sha]
    idx = 0

    def repl(m: re.Match) -> str:
        nonlocal idx
        val = f'sha256 "{shas[idx]}"'
        idx += 1
        return val

    content = re.sub(r'sha256 ".*?"', repl, content, count=2)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main() -> None:
    if len(sys.argv) < 5:
        print("Usage: update_formula.py <formula_path> <version> <arm64_sha256> <intel_sha256>", file=sys.stderr)
        sys.exit(1)

    path, version, arm_sha, intel_sha = sys.argv[1:5]
    update_formula(path, version, arm_sha, intel_sha)


if __name__ == "__main__":
    main()
