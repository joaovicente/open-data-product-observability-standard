# Developer Guide

This repository uses [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) and [mike](https://github.com/jimporter/mike) to manage documentation versioning in a way that matches the Bitol Open Data Product Standard.

## Overview

- **`schema/`**: Contains the raw JSON schemas for each version.
- **`generate_docs.py`**: A custom Python script that parses the JSON schema and converts it into the Markdown format (`docs/README.md`) using your predefined layout and tables.
- **`mike`**: An MkDocs plugin that builds your markdown files into HTML and commits them directly to the hidden `gh-pages` branch, organizing them by version folder (e.g. `/v0.0.1` and `/v0.1.0-preview`).

---

## 🏗️ 1. Modifying the Current Version (e.g., `v0.1.0-preview`)

Because your `master` branch is currently dedicated to the newest `v0.1.0-preview`, you can just make changes directly here!

1. **Edit the Schema**: Make changes to `schema/odps-observability-json-schema-v0.1.0-preview.json`.
2. **Regenerate Docs**: Run `python generate_docs.py` to recreate the Markdown tables and YAML examples inside `docs/README.md`.
3. *(Optional) Edit free-text markdown*: Modify `docs/home.md` or `docs/changelog.md` as needed.
4. **Preview Locally**: Stop the `mike` server and start a live-reloading standard MkDocs server:
   ```powershell
   mkdocs serve
   ```
5. **Lock it inside the Version**: Once you're happy with your changes, save them to Git and push them to the `mike` version selector:
   ```powershell
   git add .
   git commit -m "Updated schema tables"
   mike deploy v0.1.0-preview
   ```

---

## ⏪ 2. Modifying an Older Version (e.g., `v0.0.1`)

If you want to update the `v0.0.1` docs without bringing in your new `v0.1.0-preview` changes, you must use Git branches. By switching your Git branch back in time, `generate_docs.py` will correctly point to `v0.0.1.json`.

1. **Create a Maintenance Branch**: Checkout the commit immediately before the `v0.1.0-preview` was introduced (`c3adc26` on `master` at the time of creation):
   ```powershell
   git checkout -b release/v0.0.1 c3adc26
   ```
2. **Make your Edits**: Edit `schema/odps-observability-json-schema-v0.0.1.json` or markdown files natively on this branch.
3. **Regenerate & Deploy**:
   ```powershell
   python generate_docs.py
   git add .
   git commit -m "Fixed typo in v0.0.1"
   
   # Use --update-aliases if you want this to also overwrite the 'latest' folder shortcut!
   mike deploy v0.0.1 latest --update-aliases
   ```
4. **Return to Master**: Switch back to continue working on your new version!
   ```powershell
   git checkout master
   ```

---

## 🚀 3. Creating a Brand New Version

When `v0.1.0` is officially finalized, you'll simply follow this workflow on `master`:

1. Copy your schema: `Copy-Item schema\odps-observability-...-v0.1.0-preview.json schema\...-v0.1.0.json`
2. Update all internal strings and regular expression configurations to point to `0.1.0`.
3. Ensure `generate_docs.py` points to the new `0.1.0` JSON file.
4. Deploy the new stable release and stamp it as `latest`:
   ```powershell
   python generate_docs.py
   git add .
   git commit -m "Release v0.1.0"
   mike deploy v0.1.0 latest --update-aliases
   mike set-default latest
   ```

---

## 🙈 4. Hiding a Working Version (In Construction)

If you have a version (e.g., `v0.1.0-preview`) rapidly undergoing structural changes and you want to **hide** it from the public version dropdown until it is solid:

1. **Delete it from the Public Site:** This strictly deletes the generated HTML artifacts deployed to `gh-pages`. It **does not** delete your source code or branches:
   ```powershell
   mike delete v0.1.0
   ```
2. **Work Privately Locally:** Keep constructing the version natively on your regular branch. Use the standard MkDocs engine to preview changes locally without broadcasting them to your github pages:
   ```powershell
   mkdocs serve
   ```
3. **Show it again (Publish):** Once your work-in-progress is finalized and you are ready to reveal it into the public version selector, just deploy it normally:
   ```powershell
   mike deploy v0.1.0
   ```

---

## 🔍 5. Previewing Documentation Locally (Public vs. Private)

When working on documentation, you have two fundamentally different ways to serve your site locally:

1. **Simulate the Public GitHub Pages (`mike serve`)**
   ```powershell
   mike serve
   ```
   This spins up a local server mapping directly to the invisible `gh-pages` branch. It perfectly mimics what end users will see on the live internet. Use this to verify that your version dropdown menus, cross-version links, and published aliases (like `latest`) are rendering correctly.

2. **Simulate your Private Workspace (`mkdocs serve`)**
   ```powershell
   mkdocs serve
   ```
   This builds a live-reloading preview of your *current physical workspace* (e.g., your `master` branch) directly in memory, ignoring `mike` version structures entirely. Use this when actively writing new markdown or testing `v0.1.0-preview` structural changes under construction.
   
   *Tip: If `mike serve` is already securely running on port `8000`, you can spin this up on a different port in a second terminal to view both simultaneously:*
   ```powershell
   mkdocs serve -a localhost:8001
   ```
