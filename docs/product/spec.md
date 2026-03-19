# Product Specification: Multi-User Hugo Family Site (v1.0)

> **Location in repo:** `docs/product/spec.md`  
> **Status:** Draft  
> **Audience:** Human developers and AI agents working in this repository  

---

## 1. Purpose and Vision

This repository builds a statically generated, multi-user personal website hosted on GitHub Pages. It is powered by Hugo and built entirely from first principles — no themes, no CSS frameworks, no Tailwind. Every layout, partial, shortcode, and stylesheet is written in this repository and owned by this project.

The site serves as a shared home for up to six individual users. Each user has an independent space — a blog, a resume/about page, optional galleries, and curated social links — while sharing a common visual shell, color system, and navigation chrome.

The site is also explicitly a **playground and demonstration artifact**. AI agents working in this repository are expected to create and maintain example content that exercises every feature described in this specification. The quality of that example content is part of the quality of the project.

---

## 2. Terminology Reference

These terms are used precisely throughout this specification and all agent instructions.

| Term | Definition |
|---|---|
| **User** | One of up to six individuals with their own section of the site. Configured entirely in `data/users/`. |
| **Tag** | A single keyword attached to a blog post (e.g., `linux`, `programming`). Hugo's taxonomy term. Plural: **tags**. |
| **Taxonomy** | Hugo's classification system. This project uses one taxonomy: `tags`. The plural form `tags` is used in Hugo config. |
| **Term page** | The auto-generated Hugo page that lists all posts for a specific tag. |
| **Term list** | The auto-generated Hugo page that lists all tags used across the site. |
| **User section** | The Hugo content section rooted at `content/{username}/`. |
| **Partial** | A reusable Hugo HTML template fragment under `layouts/partials/`. |
| **Shortcode** | A reusable Hugo content macro under `layouts/shortcodes/`. |
| **Gallery** | A per-user optional image showcase presented as a paginated carousel. |
| **Card** | A single item in a gallery, with rich metadata and a permalink. |
| **Pill** | The visual styling for a tag label: a small rounded badge with Catppuccin Mocha coloring. |
| **Hugo Pipes** | Hugo's built-in asset pipeline. Used for SCSS compilation, fingerprinting, and JS bundling. |
| **Dark mode** | A user-toggleable color scheme. The default is dark (Catppuccin Mocha). |

---

## 3. Repository Structure

The following tree is **canonical**. Agents must not create directories or move files outside of this structure without explicit human approval. This constraint is enforced by agent instructions.

```
.
├── .agent/                        # Agent instruction files (see Section 12)
│   ├── agents.md                  # Root agent entrypoint and ground rules
│   ├── content-creation.md        # Rules for writing and maintaining example content
│   ├── scss-conventions.md        # CSS/SCSS authoring rules
│   ├── hugo-conventions.md        # Hugo template authoring rules
│   ├── ci-and-testing.md          # CI, validation, and screenshot test rules
│   └── janitor.md                 # Codebase cleanliness rules and cleanup checklist
├── .devcontainer/
│   ├── devcontainer.json          # VS Code / GitHub Codespaces dev container definition
│   └── Dockerfile                 # Dev container image (Hugo extended + Playwright + tools)
├── .github/
│   └── workflows/
│       ├── deploy.yml             # Build and deploy to GitHub Pages on main push
│       ├── ci.yml                 # Validate HTML, run Playwright tests on PRs
│       └── screenshots.yml        # Generate and commit screenshot artifacts on PRs
├── archetypes/
│   ├── default.md
│   └── blog.md                    # Front matter template for new blog posts
├── assets/
│   ├── scss/
│   │   ├── main.scss              # Root import file — imports all partials in order
│   │   ├── _tokens.scss           # Semantic custom property declarations ONLY (no values)
│   │   ├── _layout-vars.scss      # SCSS variables: breakpoints, spacing, radii, z-index
│   │   ├── themes/
│   │   │   ├── _catppuccin-mocha.scss   # Raw palette hex values as CSS custom props
│   │   │   ├── _catppuccin-latte.scss   # Raw palette hex values as CSS custom props
│   │   │   ├── _theme-dark.scss         # Maps active dark palette → semantic tokens
│   │   │   └── _theme-light.scss        # Maps active light palette → semantic tokens
│   │   ├── _reset.scss
│   │   ├── _typography.scss
│   │   ├── _layout.scss           # Page shell, header, footer, nav
│   │   ├── _landing.scss          # Root landing page (user grid)
│   │   ├── _user-landing.scss     # Per-user hub page
│   │   ├── _blog.scss             # Blog list and post pages
│   │   ├── _tags.scss             # Tag pills and term pages
│   │   ├── _gallery.scss          # Gallery carousel
│   │   ├── _quotes.scss           # Rotating quotes widget
│   │   └── shortcodes/
│   │       ├── _callouts.scss
│   │       ├── _resume.scss
│   │       └── _profile-intro.scss
│   ├── css/
│   │   ├── chroma-catppuccin-mocha.css  # Generated Chroma dark highlight theme
│   │   └── chroma-catppuccin-latte.css  # Generated Chroma light highlight theme
│   └── js/
│       ├── ui.js                  # Theme toggle, hamburger menu, UI interaction logic
│       └── quotes.js              # Rotating quotes cycling logic
├── content/
│   ├── _index.md                  # Root landing page content
│   ├── disclaimer.md
│   └── {username}/
│       ├── _index.md              # User hub page
│       ├── about/
│       │   └── index.md           # Resume/about page
│       ├── blog/
│       │   ├── _index.md          # Blog chronology list page
│       │   └── {year}/
│       │       └── {slug}/
│       │           └── index.md   # Individual blog post (leaf bundle)
│       └── gallery/               # Optional; omit if user has no gallery
│           ├── _index.md
│           └── {slug}/
│               └── index.md       # Individual gallery card (leaf bundle)
├── data/
│   └── users/
│       └── {username}/
│           ├── profile.yaml           # Per-user identity, features, social links
│           └── quotes.yaml            # Per-user rotating quotes
├── layouts/
│   ├── _default/
│   │   ├── baseof.html            # Master shell (head, header, footer)
│   │   ├── list.html
│   │   ├── single.html
│   │   └── terms.html             # Tag term list page
│   ├── index.html                 # Root landing page template
│   ├── partials/
│   │   ├── head.html              # <head> with Hugo Pipes CSS/JS
│   │   ├── header.html            # Site header with user nav links
│   │   ├── footer.html            # Site footer
│   │   ├── dark-mode-toggle.html
│   │   ├── user-card.html         # Avatar + name card for landing grid
│   │   ├── blog-card.html         # Post summary card used in list pages
│   │   ├── tag-pill.html          # Single tag rendered as a pill
│   │   ├── gallery-carousel.html
│   │   ├── quotes-widget.html
│   │   └── social-links.html      # Font Awesome social icon row
│   ├── {username}/
│   │   ├── list.html              # Per-user blog list (overrides _default)
│   │   └── single.html            # Per-user blog post (overrides _default)
│   ├── tags/
│   │   ├── list.html              # All-tags index
│   │   └── term.html              # Posts for a single tag
│   ├── gallery/
│   │   ├── list.html
│   │   └── single.html            # Individual gallery card page
│   └── shortcodes/
│       ├── note.html
│       ├── warning.html
│       ├── tip.html
│       ├── important.html
│       ├── caution.html
│       ├── resume-role.html
│       ├── resume-org.html
│       ├── profile-intro.html
│       ├── showcase.html
│       ├── list-columns.html
│       └── highlight-file.html
├── static/
│   ├── images/
│   │   └── {username}/
│   │       ├── avatar.jpg
│   │       └── headshot.jpg
│   └── fonts/                     # Self-hosted fallbacks if any
├── tests/
│   ├── playwright.config.ts
│   ├── screenshots/               # Golden screenshots committed to repo
│   │   └── {page-slug}.png
│   └── specs/
│       ├── smoke.spec.ts          # Basic page load and link checks
│       ├── navigation.spec.ts     # Header nav, user links, footer links
│       ├── tags.spec.ts           # Tag pill rendering and term page routing
│       ├── gallery.spec.ts        # Carousel render and card permalinks
│       ├── dark-mode.spec.ts      # Toggle behavior and persistence
│       └── screenshot.spec.ts     # Visual regression against golden images
├── docs/
│   ├── product/
│   │   └── spec.md                # This file
│   └── architecture/
│       └── decisions.md           # Architectural decision records (ADRs)
├── Dockerfile.hugo
├── Dockerfile.playwright
├── docker-compose.yaml
├── docker-compose.override.yaml
├── flake.nix
├── flake.lock
├── .envrc
├── Makefile
├── hugo.yaml
├── .djlintrc                          # djlint config for Hugo template formatting
├── .prettierrc.yaml                   # Prettier config for SCSS and JS
├── .prettierignore                    # Excludes templates, YAML, markdown from Prettier
├── .stylelintrc.yaml                  # Stylelint config for SCSS correctness
├── .yamllint.yaml                     # yamllint config for all YAML files
├── .eslintrc.yaml                     # ESLint config for JS files
├── .markdownlint.json                 # markdownlint config for content and docs
├── .htmlvalidate.json                 # html-validate config for generated HTML
└── README.md
```

---

## 4. Visual Design System

### 4.1 Theme Architecture — Two Layers

Color is deliberately split into two independent layers so that the palette can be swapped without touching a single component file. This is essential because color choices are subjective and will be iterated on over the life of the project.

**Layer 1 — Palette files** (`assets/scss/themes/_*.scss`)

Each palette file defines raw color values as CSS custom properties under a palette-specific namespace. The current default palettes are Catppuccin Mocha (dark) and Catppuccin Latte (light). A palette file knows nothing about how its colors are used — it is purely a named color dictionary.

```scss
// assets/scss/themes/_catppuccin-mocha.scss
// Defines --palette-* custom properties. No selectors other than :root.
:root {
  --palette-base:      #1e1e2e;
  --palette-mantle:    #181825;
  --palette-crust:     #11111b;
  --palette-surface0:  #313244;
  --palette-surface1:  #45475a;
  --palette-surface2:  #585b70;
  --palette-overlay0:  #6c7086;
  --palette-overlay1:  #7f849c;
  --palette-overlay2:  #9399b2;
  --palette-subtext0:  #a6adc8;
  --palette-subtext1:  #bac2de;
  --palette-text:      #cdd6f4;
  --palette-lavender:  #b4befe;
  --palette-blue:      #89b4fa;
  --palette-sapphire:  #74c7ec;
  --palette-sky:       #89dceb;
  --palette-teal:      #94e2d5;
  --palette-green:     #a6e3a1;
  --palette-yellow:    #f9e2af;
  --palette-peach:     #fab387;
  --palette-maroon:    #eba0ac;
  --palette-red:       #f38ba8;
  --palette-mauve:     #cba6f7;
  --palette-pink:      #f5c2e7;
  --palette-flamingo:  #f2cdcd;
  --palette-rosewater: #f5e0dc;

  /* Tag accent pool — 10 slots, drawn from the palette */
  --palette-tag-1: var(--palette-mauve);
  --palette-tag-2: var(--palette-blue);
  --palette-tag-3: var(--palette-green);
  --palette-tag-4: var(--palette-peach);
  --palette-tag-5: var(--palette-pink);
  --palette-tag-6: var(--palette-teal);
  --palette-tag-7: var(--palette-yellow);
  --palette-tag-8: var(--palette-maroon);
  --palette-tag-9: var(--palette-lavender);
  --palette-tag-10: var(--palette-sky);
}
```

**Layer 2 — Theme mapping files** (`assets/scss/themes/_theme-dark.scss`, `_theme-light.scss`)

Each theme file maps `--palette-*` tokens to `--color-*` semantic tokens under the appropriate `[data-theme]` selector. Component SCSS files reference **only** `--color-*` tokens. They never reference `--palette-*` tokens and never reference hex values.

```scss
// assets/scss/themes/_theme-dark.scss
// Reads from --palette-* and assigns to --color-*.
// To switch the dark palette, change _theme-dark.scss's @use import.
:root,
[data-theme="dark"] {
  --color-bg:              var(--palette-base);
  --color-bg-raised:       var(--palette-surface0);
  --color-bg-sunken:       var(--palette-mantle);
  --color-border:          var(--palette-surface1);
  --color-border-subtle:   var(--palette-surface0);
  --color-text:            var(--palette-text);
  --color-text-muted:      var(--palette-subtext0);
  --color-text-faint:      var(--palette-overlay1);
  --color-heading:         var(--palette-lavender);
  --color-link:            var(--palette-blue);
  --color-link-hover:      var(--palette-sapphire);
  --color-accent:          var(--palette-mauve);
  --color-accent-alt:      var(--palette-pink);
  --color-code-bg:         var(--palette-mantle);
  --color-code-text:       var(--palette-green);
  --color-callout-note:    var(--palette-blue);
  --color-callout-tip:     var(--palette-green);
  --color-callout-warning: var(--palette-yellow);
  --color-callout-caution: var(--palette-red);
  --color-callout-important: var(--palette-mauve);
  --color-tag-1:  var(--palette-tag-1);
  --color-tag-2:  var(--palette-tag-2);
  /* ... through tag-10 */
}
```

The light theme file follows the identical structure, reading from a different palette import.

**What changes when you swap a palette:**

To replace Catppuccin Mocha with Nord as the dark palette, an agent (or human) would:
1. Create `assets/scss/themes/_nord.scss` with Nord's hex values under the same `--palette-*` names.
2. In `_theme-dark.scss`, change the one `@use` import from `catppuccin-mocha` to `nord`.
3. Update `hugo.yaml` `chroma_style_dark` to the nearest matching Chroma style name.
4. Run `make build`. No component files change.

This is the only permitted method of changing the color scheme.

**The `_tokens.scss` file** documents the full semantic token vocabulary as comments with no values — it is a contract that component authors reference to know what tokens exist. Components must not use tokens that are not listed in `_tokens.scss`.

### 4.2 Dark / Light Mode Toggle

- The site defaults to **dark mode**.
- Light mode is applied via `data-theme="light"` on `<html>`. Dark mode is `data-theme="dark"` (also the `:root` fallback).
- The toggle state is persisted in `localStorage` under the key `theme`.
- The toggle button appears in the site header using a Font Awesome moon/sun icon.
- On first load, if the user has no stored preference, `prefers-color-scheme` is respected.
- The toggle is palette-agnostic. It switches between the `dark` and `light` values of `data-theme` only. It has no knowledge of which specific palette files back those themes.

### 4.3 Chroma Syntax Highlight Themes

The Chroma style for code blocks is configured separately from the site palette and must be easily swappable without touching SCSS. It is driven by two params in `hugo.yaml`:

```yaml
params:
  chroma_style_dark: "catppuccin-mocha"
  chroma_style_light: "catppuccin-latte"
```

Hugo generates two Chroma stylesheets at build time (one per style) via Hugo Pipes. The `head.html` partial emits both, with `media` attributes to activate the correct one:

```html
{{- $darkStyle  := site.Params.chroma_style_dark  | default "catppuccin-mocha" -}}
{{- $lightStyle := site.Params.chroma_style_light | default "catppuccin-latte" -}}
<link id="chroma-dark"  rel="stylesheet" media="(prefers-color-scheme: dark)"  href="...">
<link id="chroma-light" rel="stylesheet" media="(prefers-color-scheme: light)" href="...">
```

`ui.js` swaps the `media` attributes on these two elements in sync with the theme toggle, so Chroma styling always matches the active theme. To swap to a different highlight style, only `hugo.yaml` changes.

### 4.4 Typography

- **Heading font:** A serif or display-weight font with strong visual weight (e.g., Georgia, or a self-hosted option). The large heading on the reference site (`write.rog.gr`) is the visual target.
- **Body font:** System font stack. Clean, readable, no external font dependency required for body text.
- **Monospace:** System monospace stack used for code blocks and `resume-role` dates.
- Font sizes use `rem` with a `1rem = 16px` base. All sizing lives in `_typography.scss`.

### 4.5 Tag Pills

Each tag is rendered as a small rounded pill badge. Tags are color-assigned by a deterministic hash of the tag name mapped to one of ten numbered semantic tag color slots (`--color-tag-1` through `--color-tag-10`). The same tag always renders in the same color across all pages and both themes, with no manual configuration required.

The assignment is done in the `tag-pill.html` partial using a simple modulo hash on the tag name string, producing an index from 1–10 that selects the appropriate `--color-tag-N` custom property. The actual colors behind those properties are defined by the active theme — swapping the palette automatically recolors all pills.

Pills use a semi-transparent background (e.g., `color-mix(in srgb, var(--color-tag-N) 18%, transparent)`) with a 1px solid border in the full `--color-tag-N` color and text in the same full color. This pattern works correctly in both light and dark themes because the colors are always sourced from the semantic layer.

Pill CSS lives in `_tags.scss`. The pill partial is `partials/tag-pill.html`. Pill styles must not reference any `--palette-*` tokens.

### 4.6 Design Consistency Standards

Symmetry and alignment are first-class requirements. The following rules exist because asymmetry between similarly-typed elements — avatars at different sizes, nav links at different heights — is the most visually jarring failure mode this site can have. These rules must be enforced in CSS, not by convention.

**Rule: Same element type → same size, always.**

| Element type | Size constraint | Implementation |
|---|---|---|
| User avatars (landing grid) | `96px × 96px`, `border-radius: 50%`, `object-fit: cover` | Fixed in `_landing.scss`. `width` and `height` are never `auto` on avatar `<img>` elements. |
| User avatars (hub page header) | `128px × 128px`, circular | Same as above, different class. |
| Header nav links | All on the same baseline; height controlled by the `<header>` flex container, not by the links themselves | `display: flex; align-items: center` on the nav container. No individual link may set its own `height`, `line-height`, or `margin-top`. |
| Nav link font size | `1rem` for all user short names in the header, always | Never scale nav link font size dynamically to fit more names. If six names do not fit, the mobile hamburger menu takes over at `$bp-tablet`. |
| Blog post cards (list view) | Cards in a list must share identical outer dimensions; inner content scrolls or truncates, never expands the card | Achieved via a fixed `min-height` on the card and `overflow: hidden` on the summary text. |
| Gallery cards | Same fixed aspect ratio per gallery instance (configured in `data/users/{username}/profile.yaml` as `gallery_aspect_ratio`, default `"4/3"`) | Applied via `aspect-ratio` CSS property on the card image container. |

**Rule: CSS Grid is the layout primitive for all multi-item horizontal sets.**

- The landing page user grid uses `display: grid` with `grid-template-columns: repeat(auto-fill, minmax(200px, 1fr))`. Never use `float` or inline-block for multi-item grids.
- The header nav uses `display: flex` with `gap` for spacing. Never use `margin-right` hacks on individual nav items.
- Gallery card grids use `display: grid` in the same pattern as the landing page.

**Rule: Responsive sizing via CSS clamp(), not magic numbers.**

Typography that must scale across viewports uses `clamp(min, preferred, max)`. This applies to page headings and section titles. Body text and nav links do not scale — they remain at their fixed `rem` values.

**Rule: No element may hardcode its size in a way that breaks when the number of users changes.**

The site is designed for up to six users but must not break visually at two, four, or six users. Templates must not make assumptions about the user count. Grid layouts must reflow gracefully. The header must not overflow or wrap awkwardly at six names. The mobile breakpoint is the safety valve when horizontal space runs out.

---

## 5. User Partitioning Principle

**All data, content, and assets belonging to a user are grouped under that user's namespace.** This is a first-class architectural principle, not a convention.

| Layer | User namespace | Access pattern |
|---|---|---|
| Content | `content/{username}/` | Hugo section; URL prefix `/{username}/` |
| Data | `data/users/{username}/` | `site.Data.users.{username}.*` |
| Static assets | `static/images/{username}/` | URL prefix `/images/{username}/` |
| Layout overrides | `layouts/{username}/` | Hugo section template override |

**Why this matters for agents:** When creating any file related to a user, the first question must be "which user does this belong to?" The answer determines the directory. Files that span users (shared partials, global tag pages, the root landing page) live in their own directories outside any user namespace and must never contain user-specific data.

**Content partitioning (`content/{username}/`)** is enforced by Hugo's section system — the URL, the template resolution, and the taxonomy scoping all derive from the section. It is structurally impossible to accidentally put a user's blog post outside their section and have it render correctly.

**Data partitioning (`data/users/{username}/`)** requires discipline because Hugo does not enforce it structurally. The rule is: every data file that belongs to a specific user lives inside `data/users/{username}/`. There are no exceptions. Shared or global data (if any is ever added) lives in `data/global/` to make the distinction explicit.

The directory-per-user structure (rather than a flat file per user) is chosen deliberately for two reasons: it groups all of a user's data under one removable directory, and it still allows clean iteration via `range site.Data.users` in Hugo templates — ranging over `site.Data` directly would pick up non-user keys and is explicitly disallowed.

**Adding a user** means: create `data/users/{username}/`, `content/{username}/`, and `static/images/{username}/`. Nothing else.

**Removing a user** means: delete those three directories and set `enabled: false` (or remove) from `data/users/{username}/profile.yaml`. The site must build cleanly with any number of enabled users from zero to six.

---

## 6. User Data Model

Each user is configured entirely under `data/users/{username}/`. No user-specific information is hardcoded in templates.

### 6.1 Directory Structure Per User

```
data/users/{username}/
    profile.yaml      # Identity, features, social links
    quotes.yaml       # Rotating quotes for the hub page
```

Both files are required for every enabled user. Templates access them as `site.Data.users.{username}.profile` and `site.Data.users.{username}.quotes`. Iterating all users in templates is done via `range site.Data.users` — this works correctly because each value in the map is a directory (containing `profile` and `quotes` sub-keys), not a flat file.

### 6.2 Profile Schema (`data/users/{username}/profile.yaml`)

```yaml
username: "roger"
display_name: "Roger Fleig"
short_name: "Roger"             # Used in header nav — keep short
tagline: "Engineer. Tinkerer. Pedant."
avatar: "/images/roger/avatar.jpg"
headshot: "/images/roger/headshot.jpg"
enabled: true

features:
  blog: true
  about: true
  gallery: true

social:
  - platform: "github"
    url: "https://github.com/grubbyhacker"
    icon: "fab fa-github fa-2x"
    label: "GitHub"
  - platform: "linkedin"
    url: "https://linkedin.com/in/example"
    icon: "fab fa-linkedin fa-2x"
    label: "LinkedIn"
  - platform: "mastodon"
    url: "https://mastodon.social/@example"
    icon: "fab fa-mastodon fa-2x"
    label: "Mastodon"

gallery_title: "Photo Portfolio"    # Optional; only meaningful if features.gallery is true
gallery_aspect_ratio: "4/3"         # Optional; default "4/3"
```

All fields except `username`, `display_name`, `short_name`, `avatar`, and `enabled` are optional. Templates degrade gracefully when optional fields are absent.

### 6.3 Quotes Schema (`data/users/{username}/quotes.yaml`)

```yaml
quotes:
  - text: "Programs must be written for people to read, and only incidentally for machines to execute."
    attribution: "Harold Abelson"
  - text: "Simplicity is a great virtue but it requires hard work to achieve it."
    attribution: "Edsger W. Dijkstra"
  - text: "The best code is no code at all."
    attribution: "Jeff Atwood"
```

Agents must supply at least five quotes per user. Quotes should feel authentic to each user's persona.

### 6.4 Example Users

The repository ships with six example users. Agents create and maintain content for all six. The six seed users are:

| Username | Persona | Gallery type |
|---|---|---|
| `alice` | Software engineer, blogger | Photo portfolio |
| `bob` | Home baker and woodworker | None |
| `carol` | Quilter and textile artist | Quilt portfolio |
| `dave` | Photographer and traveler | Photo portfolio |
| `eve` | Security researcher and speaker | None |
| `frank` | Retro gaming hobbyist | None |

Agents may expand the persona depth for each user to make example content more realistic and interesting.

---

## 7. Site Structure and Pages

### 7.1 Root Landing Page (`/`)

- Displays a grid of user cards. Each card shows:
  - The user's avatar image
  - Their `display_name`
  - Clicking anywhere on the card navigates to `/{username}/`
- The header on this page shows the site name and short user names as nav links.
- Background: `--color-bg`. Grid is responsive; 3 columns on desktop, 2 on tablet, 1 on mobile.

### 7.2 Site Header (all pages)

- Site name or logo on the left.
- User short names as inline nav links on the right (pulled from `data/users/`; only `enabled: true` users appear).
- Dark mode toggle button (moon/sun icon).
- On mobile: hamburger menu that expands to show nav links vertically.
- Header is a `<header>` element rendered via `partials/header.html`.

### 7.3 Site Footer (all pages)

- Copyright line (year auto-generated from Hugo's `.Now.Year`).
- Link to `/disclaimer/`.
- "Powered by Hugo" text with link.
- Footer is rendered via `partials/footer.html`.

### 7.4 User Hub Page (`/{username}/`)

Rendered from `layouts/{username}/list.html` (or a parameterized generic template if per-user overrides are unnecessary).

Content:

1. **User header block** — avatar, display name, tagline.
2. **Social links row** — Font Awesome icons sourced from `data/users/{username}/profile.yaml`. Icons are `<a>` elements with `aria-label` set to the `label` field.
3. **Rotating quotes widget** — Cycles through quotes defined in `data/users/{username}/quotes.yaml`. Controlled by `assets/js/quotes.js`.
4. **Navigation tiles** — Three styled tiles linking to About, Blog, and Gallery (if enabled). Tiles use Catppuccin accent colors and Font Awesome icons.
5. **Recent posts preview** — The three most recent blog posts from this user, rendered as `blog-card` partials.

### 7.5 About / Resume Page (`/{username}/about/`)

A standard single-page layout with rich shortcode usage. Every user's about page must demonstrate at minimum:

- `profile-intro` shortcode with headshot and attribute list
- At least two `resume-role` shortcodes
- At least one `resume-org` shortcode
- At least one `note` callout shortcode

### 7.6 Blog List Page (`/{username}/blog/`)

- Paginated chronological list of posts, newest first.
- Pagination uses Hugo's built-in `.Paginator` with `paginate = 10` (configurable per-user via front matter override).
- Each post is rendered as a `blog-card` partial showing: tags (as pills), date, estimated read time, title (linked), and a truncated summary.
- The page title and subtitle use the large serif heading style inspired by the reference site.

### 7.7 Blog Post Page (`/{username}/blog/{year}/{slug}/`)

- Full post content.
- Tags rendered as pills below the post title.
- Post metadata: publish date, last modified date (if different), estimated read time.
- Syntax highlighting enabled via Hugo's built-in Chroma highlighter (see Section 10.5).
- Author byline linking back to `/{username}/`.
- Previous / Next post navigation.

### 7.8 Tag Term Page (`/tags/{tag}/`)

Lists all posts across all users that share a given tag. Each entry in the list shows the author username as a prefix so readers know whose post it is.

**Per-user tag scoping (preferred / stretch goal):** If a user clicks a tag pill while reading a post by `alice`, the preferred behavior is to navigate to `/alice/tags/{tag}/` and see only Alice's posts with that tag. This requires a per-user shadow taxonomy or a filtered term template. This feature is marked **stretch**. The global `/tags/{tag}/` behavior is the **baseline** and must work correctly first.

Implementation note: Per-user tag scoping can be approximated by adding a `layouts/{username}/tags/term.html` template that filters `.Data.Pages` to the current section. Agents should attempt this approach and document the result in `docs/architecture/decisions.md`.

### 7.9 Gallery (`/{username}/gallery/`)

Only rendered for users with `features.gallery: true`.

- A paginated carousel of gallery cards. Each card contains:
  - Title
  - A primary image
  - A short description
  - Rich metadata fields defined in the card's front matter (see Section 8.2)
  - A permalink to the card's own page (`/{username}/gallery/{slug}/`)
- The carousel component is pure HTML/CSS/JS — no external carousel library.
- Individual card pages (`/{username}/gallery/{slug}/`) contain the full metadata and a larger image view.

### 7.10 Legal Disclaimer (`/disclaimer/`)

Static page. Content in `content/disclaimer.md`. Linked from every page footer.

---

## 8. Content Front Matter Schemas

User data schemas (profile and quotes) are defined in §6. This section covers front matter schemas for content files, which live under `content/{username}/`.

### 8.1 Blog Post Front Matter

```yaml
---
title: "My Post Title"
date: "2025-01-15"
lastmod: "2025-01-20"     # optional; shown only if different from date
draft: false
tags:
  - "programming"
  - "linux"
summary: "A brief summary shown in list views. If omitted, Hugo truncates the content."
---
```

### 8.2 Gallery Card Front Matter

```yaml
---
title: "Star Trail Quilt"
date: "2024-06-01"
draft: false
image: "/images/carol/gallery/star-trail.jpg"
thumbnail: "/images/carol/gallery/star-trail-thumb.jpg"
summary: "A hand-pieced quilt using the traditional star trail block pattern."

# Rich metadata — schema varies by gallery type; all fields are optional
metadata:
  year_completed: 2024
  dimensions: "72 x 90 inches"
  technique: "Hand-pieced, machine quilted"
  materials: "100% cotton, Kona solids"
  pattern_source: "Original design"
---
```

Metadata fields are flexible per user. Templates render all `metadata` key/value pairs in a definition list. Agents should invent realistic metadata for each user's gallery type.

---

## 9. Navigation and Routing

| URL Pattern | Page |
|---|---|
| `/` | Root landing — user grid |
| `/disclaimer/` | Legal disclaimer |
| `/{username}/` | User hub page |
| `/{username}/about/` | Resume / about |
| `/{username}/blog/` | Blog chronology (paginated) |
| `/{username}/blog/{year}/{slug}/` | Individual blog post |
| `/{username}/gallery/` | Gallery carousel list |
| `/{username}/gallery/{slug}/` | Individual gallery card |
| `/tags/` | All-tags index |
| `/tags/{tag}/` | All posts with this tag (all users) |
| `/{username}/tags/{tag}/` | Posts with this tag by this user *(stretch)* |

All URLs must resolve cleanly with no trailing-slash ambiguity. `hugo.yaml` should set `canonifyURLs: false` and `relativeURLs: false`. Ugly URLs are disabled (`uglyURLs: false`).

---

## 10. Technical Specifications

### 10.1 Data Format Standard

**This repository uses YAML exclusively.** There is one data format. No TOML, no JSON.

This applies to every file in the repository that carries structured data:

| File type | Location | Format |
|---|---|---|
| Site configuration | `hugo.yaml` | YAML |
| Front matter | All content files | YAML (between `---` delimiters) |
| Data files | `data/**/*.yaml` | YAML |
| CI/CD workflows | `.github/workflows/*.yml` | YAML |
| Dev container config | `.devcontainer/devcontainer.json` | JSON (required by spec, exception noted) |

The `.devcontainer/devcontainer.json` file is the only permitted exception — the devcontainer spec requires JSON.

**YAML authoring rules for agents:**

1. **Always quote string values** unless they are unambiguously numeric or boolean by intent. This prevents YAML's implicit type coercion from misinterpreting values like `no` (parses as `false`), `yes`, `on`, `off`, `true`, `false`, port numbers, and ISO dates.

   ```yaml
   # Wrong — 'no' parses as boolean false
   country: no

   # Correct
   country: "no"

   # Wrong — could be coerced to a date
   version: 2024-01

   # Correct
   version: "2024-01"
   ```

2. **Use 2-space indentation.** Never tabs.

3. **Use block style for nested structures**, not flow style (`{key: value}` inline maps), except for very short single-entry maps where inline is clearly more readable.

4. **Hugo's official documentation uses TOML** in most examples. When an agent references Hugo docs and encounters a TOML snippet, it must translate it to YAML before using it. The translation is mechanical — TOML `[section]` becomes a YAML key with indented children; `key = "value"` becomes `key: "value"`.

5. **Validate YAML mentally before writing.** Indentation errors in YAML are silent in some tools and noisy in others. Hugo will fail to build if `hugo.yaml` is malformed. CI catches this, but it wastes a build cycle.

### 10.2 Hugo Configuration (`hugo.yaml`)

```yaml
baseURL: "https://example.com/"
languageCode: "en-us"
title: "Our Family Site"
paginate: 10
enableRobotsTXT: true
enableGitInfo: true

taxonomies:
  tag: "tags"

markup:
  goldmark:
    renderer:
      unsafe: true          # Required for shortcodes that emit raw HTML
  highlight:
    codeFences: true
    guessSyntax: true
    lineNos: false
    lineNumbersInTable: false
    # Style is NOT set here — driven by params below for easy swapping
    noClasses: false        # Emit CSS classes, not inline styles

params:
  debug: false
  dateFormat: "02 Jan 2006"
  paginateBy: 10
  chroma_style_dark: "catppuccin-mocha"
  chroma_style_light: "catppuccin-latte"
```

Note: `markup.highlight.style` is intentionally omitted from `hugo.yaml`. Setting it there would hardcode the Chroma style into Hugo's generated inline styles. Instead, `noClasses: false` causes Hugo to emit class-based markup, and the two Chroma stylesheets (dark and light) are generated separately via Hugo Pipes using the `chroma_style_dark` and `chroma_style_light` params. This is the mechanism that allows highlight theme swapping without a build config change.

### 10.3 SCSS Architecture

All SCSS is compiled via Hugo Pipes in `partials/head.html`:

```html
{{ $style := resources.Get "scss/main.scss" | toCSS | minify | fingerprint }}
<link rel="stylesheet" href="{{ $style.RelPermalink }}" integrity="{{ $style.Data.Integrity }}">
```

**Import order in `main.scss`:**

```scss
// 1. Layout variables (SCSS vars, not CSS custom props — must come first)
@use 'layout-vars' as *;

// 2. Palette and theme layers (defines all --palette-* and --color-* custom props)
@use 'themes/catppuccin-mocha';   // Layer 1: dark palette raw values
@use 'themes/catppuccin-latte';   // Layer 1: light palette raw values
@use 'themes/theme-dark';         // Layer 2: dark semantic mapping
@use 'themes/theme-light';        // Layer 2: light semantic mapping

// 3. Token contract (documentation only, no rules)
@use 'tokens';

// 4. Base reset and typography
@use 'reset';
@use 'typography';

// 5. Component styles (all reference --color-* only)
@use 'layout';
@use 'landing';
@use 'user-landing';
@use 'blog';
@use 'tags';
@use 'gallery';
@use 'quotes';

// 6. Shortcode styles
@use 'shortcodes/callouts';
@use 'shortcodes/resume';
@use 'shortcodes/profile-intro';
```

**Hard rules for all SCSS files:**

- Every SCSS file is a **partial** (prefixed with `_`) except `main.scss`.
- `main.scss` contains only `@use` directives — no rules.
- Files in `themes/` may reference raw hex values and define `--palette-*` or `--color-*` properties. All other files must not reference hex values.
- Files outside `themes/` must use only `--color-*` semantic tokens. Never `--palette-*`, never hex.
- SCSS layout variables (breakpoints, etc.) live in `_layout-vars.scss` and are accessed via `@use 'layout-vars' as *`.
- No `!important` declarations anywhere.
- No inline `style=""` attributes in templates, except where Hugo explicitly requires it (document the exception in a comment if used).
- Breakpoints defined in `_layout-vars.scss`:
  - `$bp-mobile: 480px`
  - `$bp-tablet: 768px`
  - `$bp-desktop: 1200px`
  - `$bp-wide: 1600px`

**Swapping a color scheme — complete procedure:**

1. Create `assets/scss/themes/_{palette-name}.scss` with `--palette-*` custom properties.
2. Edit `_theme-dark.scss` or `_theme-light.scss` to `@use` the new palette file.
3. Update `main.scss` imports to include the new palette file and remove the old one.
4. Update `hugo.yaml` `chroma_style_dark` or `chroma_style_light` param.
5. Run `make build`. Zero component files change.
6. Run `make screenshot-test` to generate diff images for human review.

### 10.4 JavaScript

- JavaScript is minimal. The two JS files are `ui.js` and `quotes.js`.
- Both files are included via Hugo Pipes with fingerprinting and `defer`.
- No JavaScript frameworks. No npm. No build step outside Hugo Pipes.
- All JS is vanilla ES2020+. Browser targets: last 2 major versions of Chrome, Firefox, Safari.

### 10.5 Syntax Highlighting

Hugo's built-in Chroma highlighter is used. Highlighting is activated via fenced code blocks in markdown:

````markdown
```python
def hello(name: str) -> str:
    return f"Hello, {name}!"
```
````

The `catppuccin-mocha` Chroma style is used for dark mode. Light mode uses `catppuccin-latte`. Style switching is handled by outputting both stylesheets and toggling their `media` attribute in sync with the theme toggle.

The `highlight-file` shortcode allows embedding a file from the repo with full syntax highlighting and a filename caption:

```
{{< highlight-file file="assets/scss/main.scss" lang="scss" >}}
```

### 10.6 Font Awesome

Font Awesome 6 Free is loaded from jsDelivr CDN for social icons in the user hub page:

```html
<link rel="stylesheet" 
  href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6/css/all.min.css">
```

Icons are used only for social links and the dark mode toggle. Icon classes follow the pattern `fab fa-github fa-2x` (brands) and `fas fa-moon fa-lg` (solid). Icon usage is defined in user data, never hardcoded in templates.

### 10.7 Theme Flicker Prevention

**This is a hard requirement.** The flash of unstyled or wrong-theme content that occurs when a page loads — where dark-mode users briefly see a light background, or vice versa — is unacceptable. It is caused by CSS loading after the browser has already painted using the default background color.

The solution is a synchronous, blocking inline `<script>` injected at the very top of `<head>`, before any `<link>` or `<style>` tags. This script reads the user's stored preference from `localStorage` and sets the `data-theme` attribute on `<html>` before the first paint. Because it is inline and not deferred, it blocks parsing just long enough to set the attribute — the cost is negligible (~1ms) and the benefit is zero flicker.

```html
<!-- In layouts/partials/head.html, FIRST thing inside <head> -->
<script>
  (function() {
    var stored = localStorage.getItem('theme');
    var preferred = stored
      ? stored
      : (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
    document.documentElement.setAttribute('data-theme', preferred);
  })();
</script>
```

Constraints that must never be violated:

- This script must appear before any `<link rel="stylesheet">` element.
- This script must never be `defer`ed, `async`'d, or moved to an external file.
- The full `ui.js` (which handles the toggle button) is still loaded with `defer` — it only manages user interaction, not initial paint.
- SCSS must define all `--color-*` semantic tokens under both `[data-theme="dark"]` (also `:root` as fallback) and `[data-theme="light"]` attribute selectors. This is guaranteed by the two-layer theme architecture in `assets/scss/themes/`. Setting theme via class (`.dark-mode`) is explicitly disallowed because class toggling requires JavaScript to run before the class is applied, which re-introduces flicker.
- The inline script uses only `"dark"` and `"light"` as `data-theme` values. It has no knowledge of palette names. If a palette is swapped, this script does not change.

The `_theme-dark.scss` and `_theme-light.scss` files must each define every `--color-*` token in the full semantic vocabulary, with no gaps. A missing token in one theme but not the other causes the wrong value to bleed through from the other selector.

### 10.8 Responsive Design and Mobile Support

Mobile support is not an afterthought. The site must be fully functional and visually coherent at all viewport widths from 320px to 2560px. The strategy is **desktop-first** (since the design reference is desktop-oriented) with explicit mobile overrides at defined breakpoints.

**Breakpoints** (defined as SCSS variables in `_layout-vars.scss`):

| Variable | Value | Semantic meaning |
|---|---|---|
| `$bp-mobile` | `480px` | Small phones |
| `$bp-tablet` | `768px` | Tablets, large phones landscape |
| `$bp-desktop` | `1200px` | Standard desktop |
| `$bp-wide` | `1600px` | Wide/ultrawide monitors |

**Breakpoint behaviors by component:**

| Component | Desktop | Tablet (`≤768px`) | Mobile (`≤480px`) |
|---|---|---|---|
| Root landing user grid | 3 columns | 2 columns | 1 column |
| Site header nav | Inline user name links + toggle | Hamburger menu (links hidden) | Hamburger menu |
| User hub nav tiles | 3 horizontal tiles | 3 tiles, smaller | Stacked vertically |
| Blog card list | Single column, wide | Single column, full-width | Single column, full-width |
| Blog post body | Max-width `720px`, centered | Full width, `1rem` horizontal padding | Full width, `0.75rem` horizontal padding |
| Gallery grid | 3 columns | 2 columns | 1 column |
| `profile-intro` headshot | Floated left, `200px` wide | Centered above text, `150px` | Centered above text, `120px` |
| `list-columns` | 2 or 3 columns as specified | 2 columns max | 1 column always |
| `resume-role` | Title + date on one line | Title + date on one line | Stacked (title above date) |

**Hamburger menu behavior:**

- At `≤$bp-tablet`, the header nav links are hidden and replaced by a hamburger icon (`fas fa-bars`).
- Clicking the icon toggles an `is-open` class on the `<nav>` element, which reveals the links stacked vertically in a dropdown below the header.
- The dropdown closes when: the user clicks a link, clicks outside the nav, or presses Escape.
- The hamburger toggle is implemented in `dark-mode.js` (which is renamed to `ui.js` for this reason — see agent note below).

**Agent note on `ui.js`:** The JS file previously named `dark-mode.js` handles all UI interaction: theme toggling, hamburger menu, and quotes cycling. It is named `assets/js/ui.js` (not `dark-mode.js`) to reflect this. The separate `quotes.js` file handles only the quote rotation animation. There are exactly two JS files.

**Touch targets:** All interactive elements must be at minimum `44px × 44px` on mobile, per WCAG 2.5.5. Nav links, social icons, and toggle buttons must use `padding` to achieve this without changing their visual size.

**Testing viewport sizes:** Screenshot tests capture pages at the following viewport sizes: `1280×800` (desktop), `768×1024` (tablet), `390×844` (iPhone 14 equivalent). All three must appear in the golden screenshot set.

---

## 11. Shortcode Library

All shortcodes live in `layouts/shortcodes/`. Corresponding styles live in `assets/scss/shortcodes/`.

### 11.1 Callout Shortcodes

Five callout variants. Each wraps inner markdown content in a styled box with a left accent border and a header label.

| Shortcode | Semantic color token | Default label | Icon class |
|---|---|---|---|
| `note` | `--color-callout-note` | Note | `fas fa-circle-info` |
| `tip` | `--color-callout-tip` | Tip | `fas fa-lightbulb` |
| `warning` | `--color-callout-warning` | Warning | `fas fa-triangle-exclamation` |
| `important` | `--color-callout-important` | Important | `fas fa-star` |
| `caution` | `--color-callout-caution` | Caution | `fas fa-fire` |

Usage:

```
{{< warning title="Breaking Change" >}}
This API was removed in v2. Use `newFunction()` instead.
{{< /warning >}}
```

The `title` parameter overrides the default label. If omitted, the default label is used.

### 11.2 Resume Shortcodes

**`resume-role`** — Renders a role title left-aligned and date range right-aligned on the same line:

```
{{< resume-role title="Senior Staff Engineer" dates="Jan 2021 – Nov 2024" >}}
```

**`resume-org`** — Renders an organization name with optional location and URL:

```
{{< resume-org name="Acme Corp" location="San Francisco, CA" url="https://acme.com" >}}
```

**`profile-intro`** — Renders a headshot floated left with a markdown attribute list:

```
{{< profile-intro image="/images/alice/headshot.jpg" alt="Alice's headshot" >}}
* **Role:** Principal Engineer
* **Location:** Seattle, WA
{{< /profile-intro >}}
```

### 11.3 Layout Shortcodes

**`showcase`** — A highlighted feature block with an optional image and a text body. Used for calling out projects, portfolio items, or key achievements within prose:

```
{{< showcase title="Open Source Contribution" image="/images/bob/widget.png" >}}
Contributed the widget feature to the Acme project. **2,000+ stars** on GitHub.
{{< /showcase >}}
```

**`list-columns`** — Renders a markdown list in two or three columns. Useful for skills lists on resumes:

```
{{< list-columns cols="2" >}}
- Go
- Rust
- Python
- Kubernetes
{{< /list-columns >}}
```

**`highlight-file`** — Embeds a repo file with syntax highlighting and a filename caption (described in Section 10.5).

---

## 12. CI / CD and Testing

### 12.1 Deployment Workflow (`.github/workflows/deploy.yml`)

Triggered on push to `main`. Steps:

1. Checkout with full git history (for `enableGitInfo = true`).
2. Setup Hugo (extended version, pinned to a specific version in the workflow).
3. Build: `hugo --minify --cleanDestinationDir`.
4. Deploy to GitHub Pages via `actions/deploy-pages`.

### 12.2 CI Workflow (`.github/workflows/ci.yml`)

Triggered on all pull requests. Steps:

1. Build Hugo site (same as deploy but without minify for better error messages).
2. **HTML validation:** Run [html-validate](https://html-validate.org/) against the generated `public/` directory. The configuration (`.htmlvalidate.json`) lives in the repo root.
3. **Link check:** Run a link checker (e.g., `lychee`) against internal links in the generated output.
4. **Playwright tests:** Build the site, start Hugo's built-in server, run all `tests/specs/*.spec.ts` suites.
5. Post a summary comment on the PR with pass/fail counts for each step.

### 12.3 Screenshot Workflow (`.github/workflows/screenshots.yml`)

Triggered on every pull request. Captures screenshots at three viewport sizes (desktop, tablet, mobile) and reports differences.

**Lifecycle phases — the golden bootstrap problem:**

The golden screenshot system has two distinct operational phases. The CI behavior differs between them, and agents must understand both.

**Phase 1 — Bootstrap (no goldens exist):**  
When `tests/screenshots/` is empty or a new page has no corresponding golden, agents are permitted and expected to generate initial goldens by running `make update-screenshots` and committing the results. There is no meaningful diff to show before goldens exist. The CI workflow detects missing goldens (by checking if the file exists before comparison) and treats a missing golden as "needs bootstrap" rather than "test failure." A PR that only adds new goldens is valid and does not require explicit human approval of the screenshots — the human reviews the PR diff as normal code review.

**Phase 2 — Established (goldens exist):**  
Once a golden file exists in the repo, it is the ground truth. Any PR that changes pixels on a page with an established golden triggers the following workflow:

1. Build the site from the PR branch.
2. Capture screenshots at all three viewport sizes.
3. Compare against goldens using Playwright's built-in image diff.
4. If any diff exceeds the configured threshold (`maxDiffPixelRatio: 0.02`), generate a side-by-side diff image.
5. Upload diff images as GitHub Actions artifacts.
6. Post a PR comment with embedded diff image links and a pass/fail summary table.
7. The CI check is marked **informational, not blocking** — it surfaces the diff for human review but does not automatically fail the PR. This is intentional: visual changes are often intentional (design updates) and should not hard-block merges.

**Updating established goldens:**

- Agents may update established goldens **when explicitly instructed to do so** in the task description. The instruction must specifically say "update screenshot goldens."
- Agents must never update goldens as a side effect of other work (e.g., to make a failing screenshot check green).
- `make update-screenshots` is the correct mechanism. Agents run it, review the diff themselves, and commit only if the diff matches the intended change.
- Humans reviewing a golden-update PR should examine the committed diff images (attached as artifacts) before approving.

**What is captured:**

| Page | Viewports |
|---|---|
| Root landing (`/`) | desktop, tablet, mobile |
| Each user hub (`/{username}/`) | desktop, mobile |
| A representative blog post | desktop, mobile |
| A tag term page (`/tags/{tag}/`) | desktop |
| A gallery list page | desktop, mobile |
| A gallery card page | desktop |

### 12.4 Makefile Targets

| Target | Description |
|---|---|
| `make serve` | Start Hugo dev server on `localhost:1313` |
| `make build` | Production build to `public/` |
| `make format` | Auto-fix all formattable files (SCSS, JS, templates) |
| `make format-templates` | Auto-fix Hugo templates via djlint |
| `make format-scss` | Auto-fix SCSS via Prettier |
| `make format-js` | Auto-fix JS via Prettier |
| `make lint` | Run all lint checks; exits non-zero on any failure |
| `make lint-templates` | Check templates via djlint (no auto-fix) |
| `make lint-scss` | Check SCSS via Prettier + Stylelint (no auto-fix) |
| `make lint-yaml` | Check all YAML via yamllint (no auto-fix) |
| `make lint-js` | Check JS via ESLint + Prettier (no auto-fix) |
| `make lint-md` | Check markdown via markdownlint (no auto-fix) |
| `make test` | Full Playwright test suite via Docker |
| `make test-ci` | Same, text output only |
| `make screenshot-test` | Screenshot comparison tests only |
| `make update-screenshots` | Capture new goldens (updates committed files) |
| `make validate-html` | Run html-validate against `public/` |
| `make check-links` | Run lychee link checker |
| `make devcontainer-build` | Build the dev container image |
| `make devcontainer-shell` | Open a shell inside the dev container |
| `make clean` | Remove `public/`, `resources/`, and Hugo cache |

---

## 13. Agent Instructions Overview

The `.agent/` directory contains instruction documents that govern how AI agents work in this repository. Agents must read the relevant instruction file before performing any work in its domain.

| File | When to read |
|---|---|
| `.agent/agents.md` | **Always.** Read before any task. Contains ground rules and pointers. |
| `.agent/content-creation.md` | Before creating or editing any file in `content/` or `data/`. |
| `.agent/scss-conventions.md` | Before creating or editing any file in `assets/scss/`. |
| `.agent/hugo-conventions.md` | Before creating or editing any file in `layouts/` or `archetypes/`. |
| `.agent/ci-and-testing.md` | Before creating or editing any file in `.github/workflows/` or `tests/`. |
| `.agent/janitor.md` | Consulted after every task as a post-task checklist. Also the instructions for the dedicated Janitor agent role. |

### 13.1 Ground Rules for All Agents

1. **Do not change the repository structure.** The directory tree in Section 3 is canonical. New files may only be created within existing directories and must follow the naming conventions of their directory.
2. **Do not install Hugo themes.** All layout code is original to this repository.
3. **Do not use Tailwind, Bootstrap, or any CSS framework.** All styling is raw SCSS.
4. **Do not add npm dependencies.** The JavaScript build uses Hugo Pipes only.
5. **Do not update established golden screenshots without explicit instruction.** See Section 12.3 for the full lifecycle. Bootstrapping new goldens for new pages is permitted.
6. **Always use the semantic CSS custom properties** (`--color-*`), never raw Catppuccin hex values or `--palette-*` tokens, in any file outside `assets/scss/themes/`. The `--palette-*` namespace is strictly internal to the theme layer. Violations of this rule break palette swapping and will require a codebase-wide find-and-replace to fix.
7. **All user configuration lives in `data/users/`.** Never hardcode usernames, display names, social links, or any other user data in a template.
8. **DRY — but only when the generalization is already needed.** Extract a partial, variable, or mixin when the same pattern appears in two or more places that will clearly need to stay in sync. Do not pre-emptively abstract things on the assumption they might be reused. Premature generalization adds indirection without benefit and makes the codebase harder to read.
9. **Leave no residue.** When fixing a bug, changing a feature, or refactoring, remove all code, config, content, and data that the change made obsolete. Orphaned SCSS classes, unused partials, stale data files, and commented-out template code are not acceptable. If you are unsure whether something is still needed, check before leaving it.
10. **All tooling must run in the dev container.** Any tool, script, or workflow step that an agent executes must work inside the `.devcontainer` environment. Agents must never assume local tools (Hugo, Playwright, Nix) are available on the host; they must use `make devcontainer-shell` or the equivalent Docker invocation. This ensures agents can run safely in GitHub Codespaces, CI environments, and any other sandboxed execution context — not just a developer's personal laptop.
11. **Validate your own output.** After making any change to layouts or SCSS, run `make validate-html` mentally or actually (if in a container). After any content change, confirm the Hugo build succeeds without warnings.

### 13.2 The Janitor Responsibility

Codebase cleanliness is a continuous responsibility, not a periodic cleanup event. Two mechanisms enforce this:

**Per-agent post-task checklist** (from `.agent/janitor.md`): After completing any task, every agent runs through the janitor checklist before closing their PR. The checklist covers: unused files, orphaned CSS classes, stale data, commented-out code, and template variables that are defined but never referenced.

**The Janitor agent role**: A dedicated agent persona described in `.agent/janitor.md` can be invoked independently to audit the full repository for accumulated crud. The Janitor agent does not add features — it only removes waste and documents what it removed and why. The Janitor agent should be invoked periodically (suggested: after every five feature PRs) and whenever a human notices the codebase feels cluttered.

### 13.3 Content Creation Mandate

Agents are expected to create and maintain realistic, engaging example content for all six seed users. The purpose is to exercise every feature of the site and serve as a living demonstration. Content requirements:

- Each user must have a minimum of **5 blog posts** covering at least **3 distinct tags**.
- Each user must have a complete `about/index.md` resume demonstrating all resume shortcodes.
- Each user with `features.gallery: true` must have a minimum of **6 gallery cards** with full metadata.
- Tags must be reused across users (so that global tag term pages have multiple entries from different authors).
- Quotes data must have at least **5 quotes** per user.
- Content should reflect each user's persona authentically. Blog posts should be coherent, multi-paragraph articles — not placeholder lorem ipsum.
- When the specification adds a new feature (shortcode, layout, data field), agents must update at least two users' content to demonstrate that feature.

---

## 14. Open Questions and Decisions Pending

These items require human decision before agents begin implementation. Answers should be recorded in `docs/architecture/decisions.md`.

| # | Question | Default if not answered |
|---|---|---|
| Q1 | Site title and domain for `baseURL` in `hugo.yaml` | `https://example.com` (overridden at deploy time via env) |
| Q2 | Which six real users will replace the seed personas? | Seed personas remain until replaced |
| Q3 | Per-user tag scoping (stretch goal): attempt or skip? | Attempt; fall back to global if blocked |
| Q4 | Gallery carousel: CSS-only scroll snap or minimal JS? | CSS scroll snap preferred; JS fallback |
| Q5 | Self-hosted body font or system font stack? | System font stack |
| Q6 | Should blog posts be dated by directory (`{year}/{slug}`) or flat? | Dated directory structure as specified |
| Q7 | Is a `lastmod` date line shown on blog posts? | Yes, only if `lastmod` differs from `date` |
| Q8 | Should the header on the root landing page include all user short names or just icons? | Both: icons in the hero grid, short names in the header nav |
| Q9 | Dev container base image: `mcr.microsoft.com/devcontainers/base:ubuntu` + manual installs, or a custom Hugo image? | Custom image based on `Dockerfile.hugo` extended with Playwright dependencies |

---

## 15. Out of Scope

The following are explicitly **not** in scope for this project:

- Multi-language / i18n support
- Comments system (no Disqus, Utterances, etc.)
- Search functionality
- Any server-side processing (this is a fully static site)
- Hugo themes of any kind
- Tailwind CSS or any utility-first CSS framework
- npm-based JS bundling (Webpack, Vite, etc.)
- Authentication or user-generated content
- RSS beyond what Hugo generates automatically (`/index.xml`)

---

*End of specification.*
