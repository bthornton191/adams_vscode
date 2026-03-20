---
name: prepare-release
description: 'Prepare the VS Code extension for publishing to the VS Code Marketplace and Open VSX. Use when: releasing a new version, bumping version, updating changelog, tagging a release, publishing extension. Handles version bump, CHANGELOG.md update, .vscodeignore audit, git commit, tag, and push.'
argument-hint: 'Version bump type (patch, minor, or major) and summary of changes'
---

# Prepare Release

Automate all steps needed to prepare and publish the MSC Adams VS Code extension.

## When to Use

- Publishing a new version of the extension
- User says "release", "publish", "bump version", "prepare for marketplace"

## Inputs

Ask the user (if not already provided):
1. **Version bump type**: `patch`, `minor`, or `major`
2. **Summary of changes**: What changed since the last release? If not provided, inspect recent git history to build the changelog entry.

## Procedure

### Step 1 — Determine the New Version

1. Read the current `version` field from [package.json](../../../package.json).
2. Apply the requested semver bump (patch / minor / major).
3. Confirm the new version number with the user before proceeding.

### Step 2 — Update `package.json`

1. Replace the `"version"` value in `package.json` with the new version string.
2. Do **not** change any other fields.

### Step 3 — Update `CHANGELOG.md`

1. Read [CHANGELOG.md](../../../CHANGELOG.md).
2. Add a new section **immediately after** the `# Changelog` heading and the table-of-contents block for the new version, following the existing format:
   - Add a TOC entry at the top of the TOC list: `  - [X.Y.Z (Month Dth YYYY)](#xyz-month-dth-yyyy)`
   - Add a section heading: `## X.Y.Z (Month Dth YYYY)` with today's date, placed **before** all previous version sections.
   - List changes as bullet points using the established conventions (`**Added**`, `**Fixed**`, `**Improved**`, `**Removed**`).
3. **Never** modify existing changelog entries.



### Step 4 — Audit `.vscodeignore`

1. Read [.vscodeignore](../../../.vscodeignore).
2. List all top-level files and directories in the workspace.
3. Identify any files or directories that:
   - Are **not** needed at runtime by extension users (e.g. dev configs, build scripts, test fixtures, documentation sources, CI configs).
   - Are **not** already listed in `.vscodeignore`.
4. If new entries are needed, propose them to the user and add upon approval.
5. Common candidates to check: `.agents/`, `.claude/`, `.github/`, `doc/`, `analytics.py`, `stats.*`, `tsconfig.json`, `__pycache__/`.

### Step 5 — Check `README.md`

1. Read [README.md](../../../README.md).
2. Compare the features and settings documented there against the current extension capabilities (commands in `package.json`, new providers, new settings, etc.).
3. If any newly added or removed features are not reflected in the README, propose updates to the user.
4. Pay special attention to:
   - The **Features** section — does it mention all current capabilities?
   - The **Extension Settings** section — does it list all settings from `package.json` `contributes.configuration`?
   - The **Known Issues** section — are resolved issues still listed?
5. Only make changes the user approves.
6. Don't include dev changes. Only update the README to reflect changes that affect end users of the extension.

### Step 6 — Commit, Tag, and Push

Check for unstaged changes. If there are any, ask the user if they want them included in this release commit. 
 - If yes, stage them
 - If no, proceed with only the version bump, changelog update, and .vscodeignore changes.

Run the following git operations:

```
git add package.json CHANGELOG.md .vscodeignore
git commit -m "Release vX.Y.Z"
git tag vX.Y.Z
git push
git push --tags
```

- The tag format is `vX.Y.Z` (with leading `v`).

### Step 7 — Publish (Optional)

Ask the user if they want to publish now. If yes, use the VS Code tasks:
- **"Publish to VS Code Marketplace"** — runs `vsce publish`
- **"Publish to Open VSX Registry"** — runs `npx ovsx publish`
- Or the combined **"Publish"** task that runs both.

**DO NOT PUBLISH UNLESS SPECIFICALLY REQUESTED BY THE USER.** 

## Quality Checks

Before committing, verify:
- [ ] `package.json` version matches the new version
- [ ] `CHANGELOG.md` has the new entry with correct date and version
- [ ] No old changelog entries were modified
- [ ] `.vscodeignore` has no obvious omissions
- [ ] `README.md` reflects current features and settings
- [ ] All files to be committed are correct (`git diff --staged`)

## Notes

- The extension uses semver. See existing changelog entries for format conventions.
- Date format in changelog: `Month Dth YYYY` (e.g. `March 20th 2026`). Use ordinal suffixes (1st, 2nd, 3rd, 4th, etc.).
- The `vsce package` build step is handled separately by the "Build Locally" task if a local `.vsix` is needed.
