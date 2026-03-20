# Branching Strategy and Workflow

> **Location in repo:** `docs/workflows/branching.md`  
> **Audience:** Human developers and AI agents  
> **Read this:** Before creating a branch, opening a PR, or pushing any commit.

---

## Branch Hierarchy

```text
main
 └── staging
      └── feature/*, fix/*, content/*, chore/*  (all work branches)
```

There are exactly two permanent branches. All other branches are temporary and must be deleted after their PR merges.

| Branch | Purpose | Who merges to it | Protection |
|---|---|---|---|
| `main` | Live production site — deploys automatically to GitHub Pages on every push | Human only, from `staging`, in rare deliberate releases | Branch protection: no direct push, no force push, requires PR |
| `staging` | Integration branch — all agent and human work targets this | Agents and humans, via PR that passes CI | Branch protection: no direct push, requires passing CI, requires human review |

**The deploy workflow (`deploy.yml`) is triggered only by pushes to `main`.** Pushing to `staging` builds and tests the site but does not deploy it. This means staging can accumulate multiple merged PRs before a human promotes them to main in a single release.

---

## The Rule on `main`

Nobody pushes directly to `main`. Ever. This is enforced by a GitHub branch protection rule, not just convention. The only path to `main` is a PR from `staging`, approved and merged by the repository owner.

The "severe emergency" exception mentioned informally is not a workflow — it is the absence of a workflow for a situation that should never arise on a static site. If the live site is broken, the correct fix is a PR to `staging` that passes CI, not a force push to `main`.

Agents must never:

- Push directly to `main` or `staging`
- Open a PR that targets `main`
- Attempt to bypass branch protection rules

---

## The Standard Agent Workflow

Every piece of work — a new feature, a content addition, a bug fix, a formatting correction — follows this path:

```text
1. Create a feature branch from staging
2. Do the work
3. Run make format && make lint && make build locally
4. Open a PR targeting staging
5. CI runs automatically — iterate until it passes
6. Human reviews and approves
7. Merge to staging (squash merge preferred for cleanliness)
8. Delete the feature branch
```

### Step 1 — Branch naming

Branch names use a type prefix and a short kebab-case description:

| Prefix | Use for |
|---|---|
| `feature/` | New functionality |
| `fix/` | Bug fixes |
| `content/` | Content additions or updates (blog posts, data files) |
| `chore/` | Formatting fixes, dependency updates, janitor work |
| `experiment/` | Exploratory work that may not merge |

Examples:

```text
feature/gallery-carousel
fix/header-nav-alignment
content/alice-blog-posts
chore/janitor-audit-2025-04
experiment/per-user-tag-scoping
```

Branch names must be lowercase, hyphenated, and specific enough that a human can understand the scope from the name alone. `feature/updates` is not acceptable. `feature/dark-mode-toggle` is.

### Step 2 — Always branch from `staging`

```bash
git checkout staging
git pull origin staging
git checkout -b feature/my-feature
```

Never branch from `main`. Never branch from another feature branch unless explicitly coordinating a dependency (document the dependency in the PR description if you do).

### Step 3 — Keep branches focused

One branch, one concern. A PR that adds a gallery feature, fixes a nav alignment bug, and updates Carol's blog posts is three PRs. Focused PRs are faster to review, easier to revert if something goes wrong, and produce cleaner git history.

The exception is content work: a single `content/` branch may add posts and data files for multiple users in one PR, since content changes are lower risk and human review is faster when related content arrives together.

### Step 4 — Before opening a PR

All of the following must be true before a PR is opened:

- [ ] `make build` — zero warnings, zero errors
- [ ] `make format` — run and any auto-fixable issues committed
- [ ] `make lint` — exits zero
- [ ] Branch is up to date with `staging` (`git rebase origin/staging` or `git merge origin/staging`)
- [ ] PR title is descriptive (not "Fix stuff" or "Updates")
- [ ] PR description explains what changed and why, and notes anything the reviewer should pay particular attention to

### Step 5 — CI iteration

CI runs automatically when a PR is opened or updated. If CI fails:

1. Read the failure output carefully — do not guess at fixes
2. For formatting failures: run `make format && make lint`, commit the result
3. For build failures: fix the Hugo error reported, verify locally with `make build`
4. For test failures: read the Playwright output, fix the template or content causing the failure
5. Push the fix — CI re-runs automatically
6. Repeat until CI passes

Do not mark a PR as ready for review while CI is failing. Do not ask the human reviewer to look at a PR that has not passed CI — their time is for code review, not debugging CI failures.

### Step 6 — Human review

The human reviewer (repository owner) is the only person who approves PRs to `staging`. Agents do not approve their own PRs or each other's PRs.

When a PR is ready for human review:

- CI must be passing (all checks green except the informational screenshot check)
- The branch must be up to date with `staging`
- The PR description must be complete

The reviewer may request changes. Agents address requested changes in additional commits on the same branch — do not open a new PR for review feedback.

### Step 7 — Merge strategy

**Squash merge** is preferred for all PRs to `staging`. This keeps the `staging` history linear and readable — one commit per PR, with the PR title as the commit message. The detailed commit history within the branch is preserved in the PR itself.

Exception: PRs that are purely additive content (e.g., five new blog posts with no template changes) may use a regular merge if the individual commits are already clean and meaningful.

**Never force-push to `staging` or `main`.**

### Step 8 — Branch cleanup

Delete the feature branch immediately after merge. GitHub can be configured to do this automatically. Stale branches accumulate quickly with agent workflows and make the branch list unreadable.

---

## Agent Parallelism and Worktrees

Multiple agents may work in parallel, each on their own feature branch. There is no coordination mechanism required beyond the normal PR workflow — each branch is independent until it merges to `staging`.

If an agent needs to work on two independent concerns simultaneously (e.g., adding gallery content while also fixing a CSS bug), it should use **git worktrees** rather than stashing or context-switching within a single checkout:

```bash
# From the repo root
git worktree add ../repo-gallery-content feature/gallery-content
git worktree add ../repo-fix-css fix/header-css-alignment

# Each worktree is a full independent working directory
# Work in them independently, push each branch, open separate PRs
```

Worktrees share the same `.git` directory — they are not separate clones. Agents must not run `hugo server` in two worktrees simultaneously on the same port.

When a worktree's PR has merged, remove the worktree:

```bash
git worktree remove ../repo-gallery-content
git branch -d feature/gallery-content
```

---

## Staging to Main — The Release Process

Promoting `staging` to `main` is a human action. Agents do not initiate this. The typical pattern:

1. Human reviews the state of `staging` (check CI, review recent merged PRs)
2. Human opens a PR from `staging` to `main`
3. CI runs one final time against the `main`-targeting PR
4. Human merges (no squash needed — `staging` already has clean history)
5. `deploy.yml` triggers automatically and publishes the site

There is no scheduled release cadence. The human promotes staging to main when the accumulated changes represent a coherent state worth publishing.

---

## Branch Protection Summary

For reference, these are the GitHub branch protection settings that enforce the above:

**`main`:**

- Require a pull request before merging
- Require approvals: 1 (repository owner)
- Dismiss stale pull request approvals when new commits are pushed
- Require status checks to pass before merging (`ci / build`, `ci / lint`, `ci / test`)
- Do not allow bypassing the above settings

**`staging`:**

- Require a pull request before merging
- Require approvals: 1 (repository owner)
- Require status checks to pass before merging (`ci / build`, `ci / lint`, `ci / test`)
- Do not allow force pushes
- Do not allow bypassing the above settings

---

*This document describes the intended workflow. The branch protection rules are the enforcement mechanism — this document is the explanation of why those rules exist and how to work within them.*
