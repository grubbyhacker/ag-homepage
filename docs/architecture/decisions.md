# Architecture Decision Records

> **Location in repo:** `docs/architecture/decisions.md`  
> **Audience:** Human developers and AI agents  
> **Updated by:** Agents (for decisions and blockers), Janitor agent (for audit reports), humans (for final calls on pending decisions)

---

## How to Use This File

This file is the single written record of every significant architectural decision, agent-discovered blocker, and periodic janitor audit in this repository. It is append-only — entries are never edited once they reach `Status: Accepted` or `Status: Resolved`. Superseded decisions get a new entry that references the old one.

### Entry types

There are four entry types. Use the correct heading prefix so they are easy to scan:

| Prefix | When to use |
|---|---|
| `## Decision:` | A conscious architectural choice, made by human or agent, with reasoning |
| `## Pending:` | An open question from the spec that requires human input before work can proceed |
| `## Problem:` | An agent-discovered blocker — something in the spec that cannot be implemented as written |
| `## Janitor Audit:` | A periodic cleanup audit report from the Janitor agent |

### Who writes what

- **Agents** write `Decision:` entries when they make a significant implementation choice not explicitly specified (e.g., choosing between two equally valid Hugo approaches). They write `Problem:` entries when they hit a genuine blocker. They must stop work on the blocked area and wait for human resolution.
- **Humans** resolve `Pending:` entries by editing the entry status and adding a resolution note, then opening a follow-up PR or task.
- **The Janitor agent** appends `Janitor Audit:` entries after each full audit run.

### Decision entry format

```markdown
## Decision: {short title}

- **Date:** YYYY-MM-DD
- **Status:** Accepted | Superseded by Decision: {title}
- **Decided by:** {Agent name or "Human"}
- **Affects:** {list of files or areas}

### Context
What situation prompted this decision. What alternatives were considered.

### Decision
What was decided and why.

### Consequences
What this makes easier, what it makes harder, what must now be true.
```

---

## Decisions Made During Specification (Pre-implementation)

These decisions were made during the specification writing process. They are recorded here so that agents have the full reasoning, not just the rule.

---

## Decision: YAML as the sole data format

- **Date:** 2025-03-19
- **Status:** Accepted
- **Decided by:** Human
- **Affects:** `hugo.yaml`, all `data/` files, all content front matter, all `.github/workflows/` files

### Context
Hugo supports three configuration formats: TOML, YAML, and JSON. Hugo's own documentation defaults to TOML because it is less susceptible to indentation errors when edited by humans. The project also uses YAML in CI workflows, data files, and devcontainer configuration. Two formats in one repository requires context-switching and creates inconsistency.

The primary authors of configuration in this repository are AI agents, not humans typing by hand. The principal advantage of TOML (indentation-error resistance) does not apply to agent-generated files.

### Decision
YAML exclusively, for all structured data files. The single exception is `.devcontainer/devcontainer.json`, which is required to be JSON by the devcontainer specification.

### Consequences
- All Hugo documentation examples (which use TOML) must be translated before use. Agent instruction files explicitly call this out.
- YAML footguns (implicit type coercion of `yes`, `no`, bare dates) are addressed by the "always quote strings" rule enforced by yamllint.
- The `hugo.yaml` filename (not `hugo.toml`) must be used from project initialization.

---

## Decision: Two-layer SCSS theme architecture

- **Date:** 2025-03-19
- **Status:** Accepted
- **Decided by:** Human
- **Affects:** All files in `assets/scss/`

### Context
Color palette choices are subjective and will change over the project lifetime. If palette-specific values (`#1e1e2e`, named Catppuccin tokens) are referenced directly in component SCSS files, swapping a palette requires touching every component — a high-risk, high-effort change prone to leaving stranded values.

### Decision
Two namespaces with a strict boundary:
- `--palette-*` custom properties: raw hex values, defined only in `assets/scss/themes/_palette-name.scss` files
- `--color-*` custom properties: semantic role names, defined in `_theme-dark.scss` and `_theme-light.scss` by mapping from `--palette-*`

Component files use only `--color-*`. Swapping a palette touches only the palette file and the two theme mapping files — zero component files change.

### Consequences
- Adding a new semantic color token requires updating `_tokens.scss` (contract), `_theme-dark.scss`, and `_theme-light.scss` atomically — three files, always together.
- Stylelint enforces the boundary: `color-no-hex` blocks hex values outside `themes/`, and `custom-property-pattern` flags non-conforming property names.
- A palette that has no analog for a required semantic role (e.g., a monochrome palette without distinct accent colors) must make explicit decisions about which palette values to map to which semantic roles, documented in a comment.

---

## Decision: Directory-per-user data structure

- **Date:** 2025-03-19
- **Status:** Accepted
- **Decided by:** Human
- **Affects:** `data/users/`, all Hugo templates that iterate users

### Context
Two structural options were considered:
1. Flat files: `data/users/alice.yaml` containing all per-user data
2. Directory-per-user: `data/users/alice/profile.yaml`, `data/users/alice/quotes.yaml`

Option 1 is simpler but places all user data in a single file that grows without bound as features are added. Option 2 maps cleanly to Hugo's `site.Data` structure — `site.Data.users.alice` becomes a map with `profile` and `quotes` sub-keys — while grouping all of a user's data under one removable directory.

A third option (`data/{username}/`) was rejected because ranging over `site.Data` directly would pick up non-user top-level keys, making templates fragile to future data additions.

### Decision
Directory-per-user under `data/users/{username}/`. Required files per user: `profile.yaml` and `quotes.yaml`. Templates iterate via `range site.Data.users`.

### Consequences
- Adding a user = create `data/users/{username}/` with both files.
- Removing a user = delete the directory (plus content and static image directories).
- Templates must handle the case where a user directory exists but `profile.yaml` has `enabled: false` — the range still sees the user, the `if .enabled` check gates rendering.

---

## Decision: Theme flicker prevention via blocking inline script

- **Date:** 2025-03-19
- **Status:** Accepted
- **Decided by:** Human
- **Affects:** `layouts/partials/head.html`, `assets/js/ui.js`

### Context
Dark/light theme preference is stored in `localStorage`. If the preference is applied by JavaScript loaded with `defer` or as an external file, the browser paints the default (light) background before the script runs, causing a visible flash on every page load for dark-mode users. This is a well-known problem with CSS custom property-based theme systems.

Two approaches were considered:
1. Inline blocking script in `<head>` that sets `data-theme` before any stylesheet is parsed
2. Using `prefers-color-scheme` media queries only, with no JavaScript involvement

Option 2 was rejected because it removes user control — the toggle button cannot override the OS-level preference without JavaScript involvement.

### Decision
A small synchronous inline script is the first element inside `<head>`, before any `<link>` tags. It reads `localStorage` and sets `data-theme` on `<html>` before the first paint. The `defer`red `ui.js` handles the toggle button at runtime.

### Consequences
- The inline script is intentionally render-blocking for ~1ms. This is acceptable — the alternative is a visible flash on every page load.
- The script must never be moved, deferred, or extracted to an external file. This is enforced by a comment in `head.html` and in the Hugo conventions agent instruction.
- The script is palette-agnostic: it only knows `"dark"` and `"light"`. Palette swaps do not affect it.

---

## Decision: djlint for Hugo template formatting with explicit suppression policy

- **Date:** 2025-03-19
- **Status:** Accepted
- **Decided by:** Human
- **Affects:** All files in `layouts/`, `.djlintrc`, CI workflow

### Context
Prettier does not support Go template syntax and will mangle `{{ }}` expressions. djlint is the only actively maintained formatter that treats Hugo/Jinja template expressions as opaque tokens while reformatting the surrounding HTML structure.

djlint achieves approximately 90% automated coverage — a small number of template patterns involving whitespace-control characters (`{{-` / `-}}`) and `<pre>` blocks require manual suppression annotations to prevent semantically incorrect reformatting.

### Decision
djlint is the formatter for all `layouts/` files, configured in `.djlintrc`. Three suppression categories are explicitly defined in `.agent/hugo-conventions.md`: inline content with dash-trimmed expressions, `<pre>`/`<code>` blocks, and shortcodes with `markdownify`. All suppressions require an explanatory comment directly above them.

A human-maintained style guide in `.agent/hugo-conventions.md` covers the conventions djlint does not enforce: attribute ordering, variable naming, comment format, and blank line rules.

### Consequences
- Formatting violations block CI the same way build errors do.
- Agents auto-iterate on formatting failures: `make format` first, `make lint` to identify residuals, manual fixes for the three suppression categories.
- Suppressions accumulate over time and are reviewed in janitor audits. An unusual density of suppressions in a file is a refactoring signal.

---

## Decision: Screenshot testing is informational, not blocking

- **Date:** 2025-03-19
- **Status:** Accepted
- **Decided by:** Human
- **Affects:** `.github/workflows/screenshots.yml`, `tests/specs/screenshot.spec.ts`

### Context
Visual regression tests catch unintended visual changes but also flag intentional ones (design updates). Making screenshot diffs a hard blocking check would serialize all design work — every palette swap, layout adjustment, or typography change would require a human to explicitly update goldens before the PR could merge.

### Decision
Screenshot diffs are surfaced as informational artifacts (side-by-side diff images uploaded to GitHub Actions artifacts, and a summary comment on the PR) but do not block merge. The check is still present and always runs — it is the hard-block status that is removed.

Phase 1 (bootstrap): agents may generate initial goldens freely when none exist for a page.
Phase 2 (established): agents may update goldens only when explicitly instructed. The instruction must say "update screenshot goldens."

### Consequences
- Visual changes can merge without explicit golden approval — the human reviewer is responsible for examining the diff comment before approving.
- Formatting and functional tests remain hard-blocking. Only the screenshot check is informational.
- This decision should be revisited once the site design stabilizes. At that point, promoting screenshot checks to blocking may be appropriate.

---

## Pending Decisions

These items are unresolved. Agents must use the stated default behavior until a human provides a resolution. When resolved, move the entry to the Decisions section above and add a resolution note.

---

## Pending: Site title and domain

- **Status:** Pending human input
- **Default behavior:** `baseURL: "https://example.com/"` in `hugo.yaml`, overridden at deploy time via `HUGO_BASEURL` environment variable
- **Question:** What is the production domain and site title?
- **Impact:** `hugo.yaml` `baseURL` and `title` fields; the legal disclaimer page; the `<title>` element on all pages

---

## Pending: Real users replacing seed personas

- **Status:** Pending human input
- **Default behavior:** The six seed personas (alice, bob, carol, dave, eve, frank) remain as the site's users until replaced
- **Question:** Which real people will be the six users? What are their usernames, display names, and short names?
- **Impact:** All of `data/users/`, all of `content/`, all of `static/images/`, the root landing page grid
- **Note:** Replacing seed users is a structured operation. The correct process is: (1) human provides the user list, (2) agent creates new data files, (3) agent migrates or discards seed content, (4) Janitor audit confirms no seed residue remains.

---

## Pending: Per-user tag scoping

- **Status:** Pending implementation attempt
- **Default behavior:** Global tags only — clicking a tag pill navigates to `/tags/{tag}/` showing all posts across all users
- **Question:** Should per-user tag scoping (`/{username}/tags/{tag}/`) be implemented?
- **Approach to attempt:** Add `layouts/{username}/tags/term.html` templates that filter `.Data.Pages` to the current user's section. If this approach is blocked by Hugo's taxonomy architecture, document the blocker here and fall back to global tags.
- **Impact:** Tag pill `href` values in blog post templates; `layouts/tags/` directory; user experience for readers who want to stay within one author's content

---

## Pending: Gallery carousel implementation

- **Status:** Pending implementation decision
- **Default behavior:** CSS scroll snap carousel (no JavaScript)
- **Question:** Is CSS scroll snap sufficient, or is a minimal JavaScript carousel required?
- **Guidance:** Attempt the CSS-only approach first. If it cannot support the required features (keyboard navigation, direct card permalink scroll-to, aria accessibility), document what CSS cannot achieve and implement the minimal JS version. The minimal JS version must still use no external carousel library.

---

## Pending: Body font selection

- **Status:** Pending human preference
- **Default behavior:** System font stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`)
- **Question:** Should a specific body font be self-hosted, or is the system font stack acceptable?
- **Impact:** `_typography.scss`; `static/fonts/` directory (currently empty); page load performance
- **Note:** The heading font is a separate concern and may be a serif regardless of this decision.

---

## Pending: Dev container base image

- **Status:** Pending implementation
- **Default behavior:** Custom image built from `Dockerfile.hugo` extended with Playwright and formatting tool dependencies
- **Question:** Should the dev container use the Microsoft devcontainer base image with manual tool installation, or a custom image derived from the existing `Dockerfile.hugo`?
- **Trade-off:** The Microsoft base image receives regular security patches and has good VS Code integration out of the box. The custom image has a smaller surface area and matches the CI container exactly. Either is acceptable — the choice affects `.devcontainer/Dockerfile` and `devcontainer.json` only.

---

## Template

Copy this block when adding a new entry:

```markdown
## Decision: {title}

- **Date:** YYYY-MM-DD
- **Status:** Accepted
- **Decided by:** {Agent role or "Human"}
- **Affects:** {files or areas}

### Context
{What situation, what alternatives were considered}

### Decision
{What was decided and why}

### Consequences
{What this enables, what it constrains, what must now be true}
```

```markdown
## Problem: {title}

- **Date:** YYYY-MM-DD
- **Status:** Blocked — awaiting human input | Resolved by Decision: {title}
- **Reported by:** {Agent role}
- **Blocking:** {description of what work is stopped}

### What was attempted
{What the spec says, what was tried}

### Why it does not work
{Specific Hugo behavior, template limitation, or structural conflict}

### Proposed alternatives
1. {Option A — brief description}
2. {Option B — brief description}
```

```markdown
## Janitor Audit: {date}

- **Date:** YYYY-MM-DD
- **Triggered by:** {scheduled / human request}

### Findings

| Audit | Found | Removed | Deferred |
|---|---|---|---|
| Orphaned SCSS classes | N | N | N |
| Unused partials | N | N | N |
| Stale data files | N | N | N |
| Commented-out template code | N | N | N |
| Duplicate layout overrides | N | N | N |
| Front matter drift | N | N | N |
| Static image orphans | N | N | N |
| Build warnings | N | N | N |

### Deferred items
{For each deferred item: what it is, why it was not removed}

### Post-cleanup build status
`make build` — {zero warnings, zero errors / describe any remaining issues}
```

---

*This file is append-only for accepted and resolved entries. Pending entries may be edited until resolved.*
