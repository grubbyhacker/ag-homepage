# Agent Ground Rules

> **Location in repo:** `.agent/agents.md`  
> **Read this:** Before every task, unconditionally.

---

## You Are Working In a Hugo Static Site

This repository builds a multi-user static website using [Hugo](https://gohugo.io). There are no servers, no databases, no runtime processes. Everything Hugo produces is a file. Understanding this is prerequisite to all other understanding.

The full product specification lives at `docs/product/spec.md`. When this file and the spec conflict, raise the conflict rather than picking one silently. Do not resolve ambiguity by guessing.

---

## Before You Write a Single File

Read the domain instruction file that covers your task:

| If you are touching... | Read this first |
|---|---|
| `content/` or `data/` | `.agent/content-creation.md` |
| `assets/scss/` | `.agent/scss-conventions.md` |
| `layouts/`, `archetypes/`, `hugo.yaml` | `.agent/hugo-conventions.md` |
| `.github/workflows/` or `tests/` | `.agent/ci-and-testing.md` |
| Anything, at the end of your task | `.agent/janitor.md` (post-task checklist) |
| Before opening any PR | `docs/workflows/branching.md` |

If your task spans multiple domains, read all relevant files before starting.

---

## The Twelve Ground Rules

These apply to every agent on every task. No exceptions.

**1. Do not change the repository structure.**  
The directory tree in `docs/product/spec.md §3` is canonical. New files may only be created within existing directories and must follow the naming conventions of their directory. If a task genuinely requires a new directory, stop and flag it for human review.

**2. Do not install Hugo themes.**  
All layout code is original to this repository. If you find yourself reaching for a theme to solve a problem, the solution is to write the layout yourself.

**3. Do not use Tailwind, Bootstrap, or any CSS framework.**  
All styling is raw SCSS. See `.agent/scss-conventions.md` for how to do this correctly.

**4. No runtime npm dependencies.**
The JavaScript build uses Hugo Pipes only — no npm packages are bundled into the site. A `package.json` exists for dev-tooling dependencies (linters, formatters, Playwright) that run exclusively in the dev container. It must remain `private: true` with `devDependencies` only. Do not add `dependencies`, `peerDependencies`, or any package that would ship to the browser.

**5. YAML everywhere.**  
This repository uses YAML as its single data format — for `hugo.yaml`, all front matter, and all `data/` files. No TOML, no JSON (except `.devcontainer/devcontainer.json`, which is required by spec). When Hugo documentation shows TOML examples, translate them to YAML before using them. See `docs/product/spec.md §10.1` for YAML authoring rules.

**6. Semantic CSS tokens only, outside `assets/scss/themes/`.**  
Use `--color-*` custom properties. Never use `--palette-*` tokens or raw hex values outside of `assets/scss/themes/`. A violation here breaks the entire palette-swapping architecture and requires a repo-wide find-and-replace to fix.

**7. All user data lives in `data/users/{username}/`.**  
Never hardcode a username, display name, avatar path, social link, or any other user-specific value in a template. Everything user-specific is read from `data/users/{username}/profile.yaml` or `data/users/{username}/quotes.yaml`. Templates iterate users via `range site.Data.users`.

**8. Strict user partitioning.**
Every file that belongs to a user lives under that user's namespace:

- Content → `content/{username}/`
- Data → `data/users/{username}/`
- Static assets → `static/images/{username}/`
- Layout overrides → `layouts/{username}/`

Files that span users (shared partials, global tag pages) live outside all user namespaces and must contain no user-specific data.

**9. DRY — but only when the duplication is already real.**  
Extract a partial, SCSS mixin, or data variable when the identical pattern appears in two or more places that will clearly need to stay in sync. Do not pre-emptively generalize. If you are abstracting something that currently exists in only one place, you are probably making the codebase harder to read, not easier.

**10. Leave no residue.**  
When you fix a bug, change a feature, or refactor anything, remove all code, config, content, and data that the change made obsolete. Orphaned SCSS classes, unused partials, stale data files, commented-out template blocks, and dead layout overrides are not acceptable. When in doubt whether something is still needed, check all its call sites before leaving it.

**11. All tooling runs in the dev container.**  
Agents must never assume that Hugo, Playwright, or any other tool is available on the host machine. Every command must work inside `.devcontainer/`. Use `make devcontainer-shell` to get a shell, or invoke tools via `docker compose run`. This ensures the work runs safely in CI, Codespaces, and any other sandboxed environment.

**12. Format and lint before every commit. Fix formatting failures automatically.**  
Formatting errors are blocking CI failures — they prevent merge exactly as a build error does. Before opening or updating a PR, always run:

```bash
make format   # auto-fixes SCSS, JS, and HTML templates where possible
make lint     # checks all layers; exits non-zero if anything remains
```

**Agent auto-iteration protocol for formatting failures:**  
When CI reports a formatting failure, agents must iterate until it is resolved — do not leave a PR open with a known formatting failure and wait for human intervention.

1. Run `make format` — auto-fixes everything that can be auto-fixed (SCSS and JS via Prettier, HTML templates via djlint)
2. Run `make lint` — identifies anything that could not be auto-fixed
3. For each remaining failure, by type:
   - **YAML failures** (yamllint): lint-only — no auto-fix exists. Read the error, fix the YAML by hand, re-run `make lint-yaml`
   - **Stylelint failures**: almost always a rule violation (`!important`, wrong token namespace, nesting too deep) — fix the SCSS, not the config
   - **djlint residual failures**: usually a whitespace-control conflict — add a `{# djlint:off #}` / `{# djlint:on #}` block around the specific lines and explain why in a comment directly above it (see `.agent/hugo-conventions.md`)
4. Commit once `make lint` exits zero

Never disable a lint rule globally to make a check pass. File-level or block-level suppressions are permitted only when the formatter's output would be semantically incorrect. Every suppression must have a comment explaining why.

---

## What Agents Are Expected to Produce

Agents are not just implementers — they are also the content creators for this site. The site ships with six seed users whose content is entirely agent-generated. That content is expected to be realistic, coherent, and feature-complete. "Lorem ipsum" placeholder text is never acceptable. See `.agent/content-creation.md` for the full mandate.

---

## How to Signal Problems

If you encounter any of the following, stop and document the issue rather than working around it silently:

- A conflict between this file and `docs/product/spec.md`
- A Hugo behavior that makes a specified approach impractical
- A task that requires creating a new directory
- Ambiguity about which user a file belongs to
- A template that cannot be written without hardcoding user data

Document the issue in `docs/architecture/decisions.md` with the heading `## Problem: <short description>`, describe what you found and why it blocks the specified approach, and propose at least one alternative. Then stop and wait for human input before proceeding with the blocked part of the task.

---

## Bootstrapping Build Order

The repo starts from a bare scaffold. Files must be created in dependency order — later layers depend on earlier ones. Follow this sequence for initial implementation:

### Phase 1 — Foundation (no Hugo build possible yet)

1. `hugo.yaml` — site configuration must exist before anything else
2. `data/users/{username}/profile.yaml` and `quotes.yaml` for all six users — templates read from these, so they must exist before templates are written
3. `assets/scss/_layout-vars.scss` — SCSS variables referenced by all component files
4. `assets/scss/themes/` — palette and theme mapping files (all four files)
5. `assets/scss/_tokens.scss` — the semantic token contract

### Phase 2 — Core layouts (build will succeed after this phase)

1. `assets/scss/main.scss` — root import file
2. `assets/scss/_reset.scss` and `assets/scss/_typography.scss` — base styles
3. `layouts/_default/baseof.html` — the master shell; every page depends on this
4. `layouts/partials/head.html` — CSS/JS pipeline, theme flicker prevention
5. `layouts/partials/header.html` and `footer.html` — site chrome
6. `layouts/index.html` — root landing page
7. `content/_index.md` — root landing page content
8. `assets/scss/_layout.scss` — header, footer, main shell styles

### Phase 3 — User pages and components

1. `layouts/partials/user-card.html` and `assets/scss/_landing.scss` — landing grid
2. User hub page template and `assets/scss/_user-landing.scss`
3. Blog list and single templates, `assets/scss/_blog.scss`
4. `layouts/partials/tag-pill.html` and `assets/scss/_tags.scss`
5. `layouts/partials/blog-card.html`
6. `assets/js/ui.js` and `assets/js/quotes.js`

### Phase 4 — Content and extras

1. Blog posts for all six users (minimum 5 per user)
2. About pages with shortcode usage
3. Shortcode templates and `assets/scss/shortcodes/`
4. Gallery templates and content (Alice, Carol, Dave only)
5. `content/disclaimer.md`
6. Taxonomy templates (`layouts/tags/`)

### Phase 5 — Validation

1. `make build` must succeed with zero warnings
2. All pages render correctly at desktop, tablet, and mobile viewports
3. Tag term pages show posts from multiple authors

Each phase should be a separate PR (or a small number of focused PRs). Do not attempt to build everything in one branch.

---

## How Hugo Works — The Mental Model Every Agent Needs

Hugo is a template engine that maps a content tree to a URL tree. Understanding the mapping is the foundation of all correct template work.

**Content → URLs:**  
A file at `content/alice/blog/2025/my-post/index.md` produces a page at `/alice/blog/2025/my-post/`. The directory structure *is* the URL structure. Never fight this.

**Sections:**  
A directory with a `_index.md` is a Hugo section. Sections have list templates. `content/alice/` is the `alice` section. `content/alice/blog/` is the `blog` section nested inside `alice`. Section templates are looked up in `layouts/{section}/` or fall back to `layouts/_default/`.

**Data:**  
`site.Data` mirrors `data/` exactly. `data/users/alice/profile.yaml` is accessible as `site.Data.users.alice.profile`. Ranging over `site.Data.users` gives you one entry per user directory — each entry is itself a map with `profile` and `quotes` keys.

**Taxonomies:**  
The `tags` taxonomy is configured in `hugo.yaml`. Hugo auto-generates term list pages at `/tags/` and term pages at `/tags/{tag}/`. Custom templates for these live in `layouts/tags/`.

**Hugo Pipes:**  
`resources.Get "scss/main.scss" | toCSS | minify | fingerprint` compiles SCSS, minifies the output, and adds a content hash to the filename. The fingerprinted URL is available as `.RelPermalink`. This is the only CSS build pipeline in this project.

**Partials:**  
`{{ partial "header.html" . }}` renders `layouts/partials/header.html` with the current page context (`.`). Partials can return values with `return`. Pass only the context a partial needs — do not pass the entire page context to a partial that only needs one field.

**Shortcodes:**  
`{{< note >}}content{{< /note >}}` invokes `layouts/shortcodes/note.html`. Named parameters are accessed with `.Get "paramname"`. Inner content is accessed with `.Inner`, which should almost always be piped through `| markdownify`.

---

*This file was last updated to match `docs/product/spec.md` version 1.0.*
