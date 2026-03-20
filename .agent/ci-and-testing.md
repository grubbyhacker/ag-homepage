# CI, Validation, and Testing

> **Location in repo:** `.agent/ci-and-testing.md`  
> **Read this:** Before creating or editing any file in `.github/workflows/` or `tests/`.  
> **Also read:** `.agent/agents.md` first, unconditionally.

---

## Overview of the CI Stack

Three GitHub Actions workflows govern quality gates for this repository. Each has a distinct role and distinct trigger conditions.

| Workflow | File | Trigger | Blocking? |
|---|---|---|---|
| Deploy | `deploy.yml` | Push to `main` | Yes — failed deploy blocks the site |
| CI | `ci.yml` | Every pull request | Yes — failed CI blocks merge |
| Screenshots | `screenshots.yml` | Every pull request | No — informational diff only |

All workflows run inside containers. No workflow step may assume the host has Hugo, Node, or any other tool installed outside of the container image.

---

## CI Workflow (`ci.yml`)

The CI workflow is the quality gate for every PR. It must pass before merge. It runs five checks in sequence:

### Step 1 — Format and lint

All formatting and linting checks run first. A formatting failure is treated identically to a build failure — it blocks merge.

```yaml
- name: Format check — SCSS and JS
  run: npx prettier --check "assets/scss/**/*.scss" "assets/js/**/*.js"

- name: Format check — Hugo templates
  run: djlint layouts/ --check --profile=jinja

- name: Lint — SCSS
  run: npx stylelint "assets/scss/**/*.scss"

- name: Lint — YAML
  run: yamllint -c .yamllint.yaml .

- name: Lint — JS
  run: npx eslint "assets/js/**/*.js"

- name: Lint — Markdown
  run: npx markdownlint "content/**/*.md" "docs/**/*.md" ".agent/**/*.md"
```

When this step fails, agents must run `make format && make lint` locally (in the dev container), fix any remaining issues that cannot be auto-fixed, and push the corrected files before the PR can proceed. See `.agent/agents.md §Ground Rule 12` for the full auto-iteration protocol.

### Step 2 — Hugo build

```yaml
- name: Build site
  run: hugo --cleanDestinationDir
```

No `--minify` flag here — minification obscures error messages. The build must produce zero warnings. A warning about a missing template, a broken partial reference, or an undefined variable is a failure.

### Step 3 — Link check

Run `lychee` against the generated `public/` directory for internal links only. External links are excluded from CI to avoid flakiness from network conditions.

```yaml
- name: Check internal links
  run: lychee --offline --include-fragments public/
```

A broken internal link is a build error. Common causes:

- A blog post links to `/alice/blog/2025/old-post/` and that post was renamed or removed
- A partial generates a URL using a variable that can be empty
- A gallery card links to an image path that does not match the `static/images/` structure

### Step 4 — Playwright functional tests

The Playwright suite covers behavior that HTML validation cannot catch — JavaScript interaction, navigation correctness, and Hugo template logic expressed in rendered output.

```yaml
- name: Run Playwright tests
  run: make test-ci
```

Test files live in `tests/specs/`. Each file covers one area:

| Spec file | What it tests |
|---|---|
| `smoke.spec.ts` | Every top-level URL returns HTTP 200; no console errors on load |
| `navigation.spec.ts` | Header nav links resolve correctly; footer links resolve; user hub nav tiles work |
| `tags.spec.ts` | Tag pills render on blog posts; clicking a pill navigates to the correct term page; term page lists the correct posts |
| `gallery.spec.ts` | Gallery list renders cards; each card has a working permalink; metadata is present on card pages |
| `dark-mode.spec.ts` | Toggle switches theme; `data-theme` attribute is set correctly; preference persists across navigation; no flicker on load |
| `screenshot.spec.ts` | Visual regression against golden images (see Screenshot Workflow below) |

### Writing new Playwright tests

When a new page or feature is added, the spec file for the relevant area must be updated. If no existing spec covers the new feature, create one in `tests/specs/`.

Tests must:

- Start from a clean browser state (no stored `localStorage`)
- Use `page.goto()` with the full URL path
- Assert on visible content, not on implementation details (class names that could change)
- Clean up any `localStorage` state they set

```typescript
// Good — asserts on user-visible content
await expect(page.locator('.tag-pill')).toHaveText('programming');

// Bad — asserts on internal class name that could be refactored
await expect(page.locator('.tag-pill--3')).toBeVisible();
```

Dark mode tests must verify the absence of flicker, not just the final state:

```typescript
test('no theme flicker on page load', async ({ page }) => {
  // Set dark preference in localStorage before navigation
  await page.addInitScript(() => {
    localStorage.setItem('theme', 'dark');
  });
  
  // Capture the theme attribute before any scripts run
  let themeBeforeLoad = '';
  page.on('domcontentloaded', async () => {
    themeBeforeLoad = await page.getAttribute('html', 'data-theme') ?? '';
  });
  
  await page.goto('/');
  expect(themeBeforeLoad).toBe('dark'); // Must be set before DOMContentLoaded
});
```

---

## Screenshot Workflow (`screenshots.yml`)

The screenshot workflow is **informational only**. It never blocks a merge. Its purpose is to surface visual diffs for human review.

### Phase 1 — Bootstrap (no goldens exist)

When `tests/screenshots/` is empty or a specific golden does not exist yet, agents may and should generate the initial golden by running:

```bash
make update-screenshots
```

Commit the generated screenshots in the same PR that introduces the page. A PR that only adds golden screenshots is always valid — the human reviewer looks at the images as part of code review.

### Phase 2 — Established goldens

Once a golden exists, the workflow:

1. Builds the site from the PR branch
2. Captures screenshots at three viewports: `1280×800` (desktop), `768×1024` (tablet), `390×844` (mobile)
3. Compares against goldens using Playwright's image diff with `maxDiffPixelRatio: 0.02`
4. Uploads side-by-side diff images as workflow artifacts
5. Posts a summary comment on the PR

**Agents must not update established goldens as a side effect of other work.** If a golden diff appears in CI after a change that was not intended to affect visual output, that is a bug — fix the code, not the golden.

Agents may update established goldens when the task description explicitly says "update screenshot goldens." In that case, run `make update-screenshots`, review the diff visually, and commit only if the diff matches the intended change.

### Golden coverage

Goldens must exist for the following pages and viewports before the site is considered production-ready:

| Page | Desktop | Tablet | Mobile |
|---|---|---|---|
| Root landing (`/`) | ✓ | ✓ | ✓ |
| Each user hub (`/{username}/`) | ✓ | — | ✓ |
| A blog post (one representative) | ✓ | — | ✓ |
| Blog list page (one user) | ✓ | — | — |
| Tag term page (`/tags/{tag}/`) | ✓ | — | — |
| Gallery list (one user) | ✓ | — | ✓ |
| Gallery card (one) | ✓ | — | — |
| Disclaimer (`/disclaimer/`) | ✓ | — | — |

"—" means no golden required for that viewport. It does not mean the page has not been tested — the smoke test covers it.

---

## Deploy Workflow (`deploy.yml`)

Agents should rarely need to edit the deploy workflow. When they do:

- The Hugo version must be pinned to a specific release (e.g., `hugo-extended_0.147.0`), not `latest`
- The deploy step uses `actions/deploy-pages` — do not replace this with a third-party action
- The build command is `hugo --minify --cleanDestinationDir --gc` — do not remove any of these flags
- Full git history must be checked out (`fetch-depth: 0`) because `enableGitInfo: true` in `hugo.yaml` requires it

---

## Dev Container Compatibility

Every Makefile target and every workflow step must work inside the dev container. Before adding a new tool to any workflow:

1. Verify the tool is available in the dev container image
2. If not, add it to `.devcontainer/Dockerfile` in the same PR
3. Test the updated container locally with `make devcontainer-build && make devcontainer-shell`

Workflow steps that require tools not in the container image will fail in CI. Do not work around this by installing tools inline in workflow steps — that makes builds slow, fragile, and non-reproducible. The correct fix is always to add the tool to the container image.

---

## Makefile — What Each Target Does

Agents running commands locally (inside the dev container) use the Makefile:

| Target | Command it runs | Use when |
|---|---|---|
| `make serve` | `hugo server -D --baseURL=http://localhost:1313` | Local development |
| `make build` | `hugo --cleanDestinationDir` | Verify the build locally |
| `make format` | Runs all auto-fixable formatters | Before every commit |
| `make format-templates` | `djlint layouts/ --reformat` | After editing any template |
| `make format-scss` | `prettier --write assets/scss/` | After editing any SCSS |
| `make format-js` | `prettier --write assets/js/` | After editing any JS |
| `make lint` | Runs all lint checks; exits non-zero on any failure | Pre-commit and in CI |
| `make lint-templates` | `djlint layouts/ --check` | Check templates without auto-fixing |
| `make lint-scss` | `prettier --check scss && stylelint scss` | Check SCSS without auto-fixing |
| `make lint-yaml` | `yamllint -c .yamllint.yaml .` | Check all YAML files |
| `make lint-js` | `eslint assets/js/ && prettier --check js` | Check JS without auto-fixing |
| `make lint-md` | `markdownlint content/ docs/ .agent/` | Check markdown structure |
| `make test` | Playwright via Docker, HTML report | Full test run, want to see report |
| `make test-ci` | Playwright via Docker, text output | Testing in a script or CI context |
| `make screenshot-test` | Playwright screenshot spec only | Verify visual changes |
| `make update-screenshots` | Playwright `--update-snapshots` | Bootstrap or intentionally update goldens |
| `make check-links` | `lychee --offline public/` | Verify internal links after a build |
| `make clean` | Remove `public/`, `resources/`, `.hugo_build.lock` | Reset before a fresh build |
| `make devcontainer-build` | Build dev container image | After changing `.devcontainer/Dockerfile` |
| `make devcontainer-shell` | Open shell in dev container | Running any of the above in isolation |

---

## What Agents Must Not Do

- Disable or skip failing tests to make CI pass — fix the code
- Hard-code environment-specific paths in workflow files
- Add `continue-on-error: true` to any CI step without human approval
- Pin workflow action versions to `@main` or `@latest` — always use a specific SHA or version tag

---

*This file was last updated to match `docs/product/spec.md` version 1.0.*
