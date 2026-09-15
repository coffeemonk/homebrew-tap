#!/usr/bin/env python3
"""
Automated updater for Homebrew formulae and casks in coffeemonk/tap.

Designed for Apple Silicon (ARM64) macOS.
Checks upstream releases on a weekly cadence without downloading large DMG/ZIP
assets unless a newer upstream version is detected.

Usage:
    python3 .github/scripts/update_tap.py [all | <target_name>]
"""

import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from typing import Dict, List, Optional, Tuple

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) HomebrewTapUpdater/1.0"


def make_request(url: str, token: Optional[str] = None) -> urllib.request.Request:
    headers = {"User-Agent": USER_AGENT}
    if token and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {token}"
        headers["Accept"] = "application/vnd.github.v3+json"
    return urllib.request.Request(url, headers=headers)


def fetch_text(url: str, token: Optional[str] = None) -> str:
    req = make_request(url, token)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def calculate_remote_sha256(url: str, token: Optional[str] = None) -> str:
    """Stream remote file directly into sha256 hasher without saving to disk."""
    print(f"    Downloading & calculating SHA256: {url}")
    req = make_request(url, token)
    hasher = hashlib.sha256()
    with urllib.request.urlopen(req, timeout=120) as resp:
        while True:
            chunk = resp.read(1024 * 1024)  # 1MB chunk
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


class Target:
    def __init__(
        self,
        name: str,
        file_path: str,
        source_type: str,  # 'github' | 'web'
        repo: Optional[str] = None,
        tag_prefix: str = "",
        web_url: Optional[str] = None,
        web_version_regex: Optional[str] = None,
        asset_url_template: str = "",
    ):
        self.name = name
        self.file_path = file_path
        self.source_type = source_type
        self.repo = repo
        self.tag_prefix = tag_prefix
        self.web_url = web_url
        self.web_version_regex = web_version_regex
        self.asset_url_template = asset_url_template

    def get_current_version(self) -> str:
        with open(self.file_path, "r", encoding="utf-8") as f:
            content = f.read()
        m = re.search(r'version "([^"]+)"', content)
        if not m:
            raise ValueError(f"Could not find version in {self.file_path}")
        return m.group(1)

    def get_latest_upstream(self, token: Optional[str]) -> Tuple[str, str]:
        """Returns (latest_version, tag_name)."""
        if self.source_type == "github":
            url = f"https://api.github.com/repos/{self.repo}/releases/latest"
            data = json.loads(fetch_text(url, token))
            tag_name = data["tag_name"]
            version = tag_name
            if self.tag_prefix and version.startswith(self.tag_prefix):
                version = version[len(self.tag_prefix) :]
            elif version.startswith("v") and not self.tag_prefix:
                version = version[1:]
            return version, tag_name
        elif self.source_type == "web":
            html = fetch_text(self.web_url, token)
            m = re.search(self.web_version_regex, html)
            if not m:
                raise ValueError(f"Could not extract version from {self.web_url}")
            version = m.group(1)
            return version, version
        else:
            raise ValueError(f"Unknown source type: {self.source_type}")

    def update_file(self, new_version: str, new_sha256: str) -> None:
        with open(self.file_path, "r", encoding="utf-8") as f:
            content = f.read()

        content = re.sub(r'version "[^"]+"', f'version "{new_version}"', content, count=1)
        content = re.sub(r'sha256 "[^"]+"', f'sha256 "{new_sha256}"', content, count=1)

        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(content)


TARGETS: Dict[str, Target] = {
    "workflowy-cli": Target(
        name="workflowy-cli",
        file_path="formula/workflowy-cli.rb",
        source_type="github",
        repo="rodolfo-terriquez/workflowy-cli",
        tag_prefix="v",
        asset_url_template="https://github.com/{repo}/releases/download/{tag}/wf-v{version}-macos-arm64",
    ),
    "comictagger": Target(
        name="comictagger",
        file_path="Casks/comictagger.rb",
        source_type="github",
        repo="comictagger/comictagger",
        tag_prefix="",
        asset_url_template="https://github.com/{repo}/releases/download/{tag}/ComicTagger-{version}-osx-10.15.7-x86_64.app.zip",
    ),
    "darktable": Target(
        name="darktable",
        file_path="Casks/darktable.rb",
        source_type="github",
        repo="darktable-org/darktable",
        tag_prefix="release-",
        asset_url_template="https://github.com/{repo}/releases/download/{tag}/darktable-{version}-arm64.dmg",
    ),
    "kindle-comic-converter": Target(
        name="kindle-comic-converter",
        file_path="Casks/kindle-comic-converter.rb",
        source_type="github",
        repo="ciromattia/kcc",
        tag_prefix="v",
        asset_url_template="https://github.com/{repo}/releases/download/{tag}/kcc_macos_arm_{version}.dmg",
    ),
    "makemkv": Target(
        name="makemkv",
        file_path="Casks/makemkv.rb",
        source_type="web",
        web_url="https://www.makemkv.com/download/",
        web_version_regex=r'href=[\'"].*?/makemkv[._-]v?(\d+(?:\.\d+)+)[._-]osx\.dmg[\'"]',
        asset_url_template="https://www.makemkv.com/download/makemkv_v{version}_osx.dmg",
    ),
}


def check_and_update(target: Target, token: Optional[str]) -> Optional[Tuple[str, str, str]]:
    """
    Checks if a target needs an update.
    Returns (target_name, old_version, new_version) if updated, else None.
    """
    print(f"\n[{target.name}] Checking for updates...")
    current_ver = target.get_current_version()
    latest_ver, tag_name = target.get_latest_upstream(token)

    print(f"    Current tap version: {current_ver}")
    print(f"    Upstream version:    {latest_ver} (tag: {tag_name})")

    if current_ver == latest_ver:
        print(f"    ✓ {target.name} is already up to date. No downloads required.")
        return None

    print(f"    ⚡ New version detected for {target.name}: {current_ver} -> {latest_ver}")

    url = target.asset_url_template.format(
        repo=target.repo,
        tag=tag_name,
        version=latest_ver,
    )
    new_sha256 = calculate_remote_sha256(url, token)
    print(f"    SHA256: {new_sha256}")

    target.update_file(latest_ver, new_sha256)
    print(f"    ✓ Updated {target.file_path} to {latest_ver}")
    return (target.name, current_ver, latest_ver)


def main() -> None:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    selected_target = sys.argv[1] if len(sys.argv) > 1 else "all"

    if selected_target != "all" and selected_target not in TARGETS:
        print(f"Unknown target: '{selected_target}'", file=sys.stderr)
        print(f"Available targets: all, {', '.join(TARGETS.keys())}", file=sys.stderr)
        sys.exit(1)

    targets_to_run = (
        list(TARGETS.values()) if selected_target == "all" else [TARGETS[selected_target]]
    )

    updated: List[Tuple[str, str, str]] = []
    errors: List[str] = []

    for target in targets_to_run:
        try:
            res = check_and_update(target, token)
            if res:
                updated.append(res)
        except Exception as e:
            print(f"    ❌ Error updating {target.name}: {e}", file=sys.stderr)
            errors.append(f"{target.name}: {e}")

    print("\n" + "=" * 50)
    print("Summary:")
    if updated:
        print(f"Updated {len(updated)} package(s):")
        for name, old_v, new_v in updated:
            print(f"  - {name}: {old_v} -> {new_v}")
    else:
        print("All packages are up to date.")

    if errors:
        print(f"Encountered {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
