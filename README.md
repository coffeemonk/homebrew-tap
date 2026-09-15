# Homebrew Tap (`coffeemonk/tap`)

Personal Homebrew tap containing custom formulae and casks.

## Add This Tap

```bash
brew tap coffeemonk/tap
```

---

## Formulae

### `workflowy-cli` (`wf`)
Command-line interface and MCP server for [Workflowy](https://github.com/rodolfo-terriquez/workflowy-cli).

```bash
brew install coffeemonk/tap/workflowy-cli
```

Once installed, run:
```bash
wf --version
wf doctor
```

---

## Casks

These macOS applications were disabled in upstream `homebrew/cask` because upstream binaries are not Apple-notarized. They are maintained here for continued access.

| Cask | Description | Upstream |
| :--- | :--- | :--- |
| **`comictagger`** | Metadata editor for digital comics (Stable 1.5.5, Intel / requires Rosetta) | [comictagger/comictagger](https://github.com/comictagger/comictagger) |
| **`comictagger@beta`** | Metadata editor for digital comics (Beta 1.6.0, native Apple Silicon `arm64`) | [comictagger/comictagger](https://github.com/comictagger/comictagger) |
| **`darktable`** | Photography workflow app and raw developer | [darktable-org/darktable](https://www.darktable.org/) |
| **`kindle-comic-converter`** | Comic and manga converter for ebook readers | [ciromattia/kcc](https://github.com/ciromattia/kcc) |
| **`makemkv`** | DVD and Blu-ray video converter / transcoder | [makemkv.com](https://www.makemkv.com/) |

### Installation

```bash
brew install --cask coffeemonk/tap/<cask-name>
```

For ComicTagger, you can choose between stable or beta:
```bash
# Stable (1.5.5 - Intel build, requires Rosetta)
brew install --cask coffeemonk/tap/comictagger

# Beta (1.6.0 - Native Apple Silicon ARM64 build)
brew install --cask coffeemonk/tap/comictagger@beta
```

#### macOS Gatekeeper / Quarantine Note

Because these builds are unsigned/unnotarized, modern macOS (Sonoma, Sequoia, etc.) may flag them as damaged or block them from opening. You can install them bypassing quarantine:

```bash
brew install --cask --no-quarantine coffeemonk/tap/<cask-name>
```

Or remove quarantine from an already installed app:

```bash
xattr -d com.apple.quarantine /Applications/<AppName>.app
```

---

## Automated Updates

Upstream releases are checked weekly via GitHub Actions (`.github/workflows/update-tap.yml`). If a newer release is detected, the workflow downloads the release assets, computes new SHA256 checksums, updates the formula or cask definition, and commits the changes.
