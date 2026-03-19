# Janitor

> **Location in repo:** `.agent/janitor.md`  
> **Read this:** At the end of every task, as a post-task checklist. Also the instructions for the dedicated Janitor agent role.  
> **Also read:** `.agent/agents.md` first, unconditionally.

---

## Two Ways This File Is Used

**1. Post-task checklist (all agents):** Every agent runs through the checklist in Section 1 before closing a PR. This takes five minutes and prevents slow accumulation of cruft.

**2. The Janitor agent role:** A dedicated Janitor agent, invoked explicitly, runs the full audit in Section 2. It does not add features, fix bugs, or change behavior. Its only output is removed code and a written record in `docs/architecture/decisions.md` of what was removed and why. Invoke it after every five feature PRs, or whenever the codebase feels cluttered.

---

## Section 1 — Post-Task Checklist (All Agents)

Run through this after every task. Check each item before opening a PR.

### SCSS

- [ ] Every CSS class I added or changed is actually used in at least one template or shortcode. (Search `layouts/` and `layouts/shortcodes/` for the class name.)
- [ ] Every `--color-*` custom property I referenced exists in `_tokens.scss`.
- [ ] I did not leave any commented-out CSS rules in the files I touched.
- [ ] I did not add any hex values outside `assets/scss/themes/`.
- [ ] I did not add any `--palette-*` references outside `assets/scss/themes/`.
- [ ] I did not add any `!important` declarations.

### Hugo templates

- [ ] Every partial I created is called from at least one template.
- [ ] Every template variable I defined (`:=`) is referenced at least once in the same template.
- [ ] I did not leave `{{/* TODO */}}` or `{{/* FIXME */}}` comments in templates.
- [ ] I did not leave commented-out template blocks in any file I touched.
- [ ] If I created a new `layouts/{username}/` override, there is a reason it cannot be expressed in `_default` with user data, and I documented that reason in `docs/architecture/decisions.md`.

### Content and data

- [ ] Every content file I created has complete, non-placeholder front matter.
- [ ] Every `data/users/{username}/` directory contains both `profile.yaml` and `quotes.yaml`.
- [ ] I did not leave any `draft: true` posts that were meant to be published.
- [ ] If I removed or renamed a content file, I checked that no other content file links to the old path.
- [ ] Image paths referenced in front matter (`image:`, `thumbnail:`, `headshot:`, `avatar:`) follow the `static/images/{username}/` convention.

### General

- [ ] `make build` runs with zero warnings and zero errors.
- [ ] `make validate-html` passes with zero errors on the generated output.
- [ ] I did not introduce any TOML syntax (verify: no `[sections]`, no `key = value` outside YAML contexts).
- [ ] Any file I modified that I no longer need a change in is reverted.

---

## Section 2 — Full Janitor Audit (Janitor Agent Role)

The Janitor agent runs these checks against the entire repository. Each check is a specific thing to look for, a way to find it, and the correct action.

### Audit 1 — Orphaned SCSS classes

**What to find:** CSS classes defined in `assets/scss/` that are never referenced in `layouts/`.

**How to find it:**
1. Extract all class names defined in `assets/scss/` (lines matching `.class-name {` or `&__element {`)
2. For each class, search `layouts/` and `layouts/shortcodes/` for the class name as a string
3. If not found, check if it is generated dynamically (e.g., `tag-pill--#{$i}` in a loop — these are valid)
4. Flag all that are neither found nor dynamically generated

**Action:** Remove the orphaned rule. If the rule exists in a component file alongside rules that are used, remove only the orphaned rule, not the whole file.

### Audit 2 — Unused partials

**What to find:** Files in `layouts/partials/` that are never called with `{{ partial "..." }}` anywhere.

**How to find it:** For each file `layouts/partials/foo.html`, search all files in `layouts/` for the string `"foo.html"`. If not found, the partial is unused.

**Action:** Remove the unused partial file. Check git history to understand why it exists — if it was recently added for a feature in progress, note that in the audit report instead of deleting it.

### Audit 3 — Stale data files

**What to find:** Files in `data/users/` that do not correspond to an enabled user in any `profile.yaml`, or `profile.yaml` files where `enabled: false` with no clear reason.

**How to find it:** List all directories in `data/users/`. For each, read `profile.yaml` and check `enabled`. Cross-reference with the list in `docs/product/spec.md §6.4`.

**Action:** Users with `enabled: false` and no corresponding content in `content/{username}/` are candidates for removal. Document the finding before deleting anything.

### Audit 4 — Commented-out template code

**What to find:** `{{/* ... */}}` comment blocks in `layouts/` files that contain real template code (as opposed to documentation comments).

**How to find it:** Search for `{{/*` in `layouts/`. Review each match. Comments that explain *why* something is done are acceptable. Comments that contain `{{` or `}}` inside them (commented-out template tags) are code graveyard.

**Action:** Remove commented-out template code. If it represents an incomplete feature, either complete it or create a GitHub issue to track it, then remove the code.

### Audit 5 — Duplicate or redundant layout overrides

**What to find:** Files in `layouts/{username}/` that are identical to or near-identical to the `_default` equivalent.

**How to find it:** For each file in `layouts/{username}/`, diff it against the corresponding `layouts/_default/` file. If the only differences are whitespace or comments, the override is redundant.

**Action:** Remove the override and verify the page still renders correctly using the `_default` fallback.

### Audit 6 — Front matter drift

**What to find:** Content files whose front matter fields do not match the schema in `docs/product/spec.md §8`.

**How to find it:** For each `content/{username}/blog/**/*.md`, check that:
- All dates are quoted strings
- `tags` is a list of quoted strings
- No unexpected fields are present (field bloat often signals an abandoned approach)

**Action:** Fix malformed front matter. Remove unexpected fields unless they are documented as intentional additions to the schema.

### Audit 7 — `static/images/` orphans

**What to find:** Image files in `static/images/{username}/` that are not referenced by any content file or data file.

**How to find it:** List all files under `static/images/`. For each, search `content/`, `data/`, and `layouts/` for the filename. If not found, it may be orphaned.

**Note:** This check has false positives — some images may be referenced by path patterns that are hard to grep. Use judgment. Do not delete images that could plausibly be in active use.

**Action:** Delete confirmed orphans. Add a `# referenced by: content/alice/about/index.md` comment to data files that reference images, to make future audits easier.

### Audit 8 — Hugo build warnings

**What to find:** Any warning output from `hugo --cleanDestinationDir`.

**How to find it:** Run `make build 2>&1 | grep -i warn`. Zero warnings is the target.

**Action:** Fix every warning. Common Hugo warnings:
- `REF_NOT_FOUND` — a `ref` or `relref` shortcode points to a page that no longer exists
- `found no layout file` — a content type has no matching template
- Deprecated config key — update `hugo.yaml` to use the current key name

### Reporting

After completing all eight audits, the Janitor agent creates or updates `docs/architecture/decisions.md` with an entry:

```markdown
## Janitor Audit — {date}

**Triggered by:** {reason — e.g., "post-5-feature-PRs scheduled audit"}

**Findings:**

| Audit | Items found | Items removed | Items deferred |
|---|---|---|---|
| Orphaned SCSS classes | N | N | N |
| Unused partials | N | N | N |
| ... | | | |

**Deferred items:** {explain why each deferred item was not removed}

**Build status post-cleanup:** `make build` — zero warnings, zero errors.
```

---

## What the Janitor Never Does

- Fixes bugs (those go in feature PRs)
- Changes behavior (CSS changes that alter visual output are feature changes, not cleanup)
- Removes code it does not understand — if in doubt, document and defer
- Deletes golden screenshots
- Updates `docs/product/spec.md` — that requires human review

---

*This file was last updated to match `docs/product/spec.md` version 1.0.*
