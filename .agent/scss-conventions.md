# SCSS Conventions

> **Location in repo:** `.agent/scss-conventions.md`  
> **Read this:** Before creating or editing any file in `assets/scss/`.  
> **Also read:** `.agent/agents.md` first, unconditionally.

---

## The Three-Namespace Rule

Every color value in this codebase belongs to exactly one of three namespaces. Placing a value in the wrong namespace breaks the palette-swapping architecture.

| Namespace | Where it lives | Who uses it |
|---|---|---|
| Raw hex values | `assets/scss/themes/_*.scss` palette files | Nobody else. Ever. |
| `--palette-*` custom props | `assets/scss/themes/_*.scss` palette files | Only `_theme-dark.scss` and `_theme-light.scss` |
| `--color-*` semantic custom props | `assets/scss/themes/_theme-*.scss` mapping files | Every component file |
| SCSS layout `$variables` | `assets/scss/_layout-vars.scss` | Every component file via `@use` |

**The hard rule:** Any file outside `assets/scss/themes/` must contain zero hex values and zero `--palette-*` references. Violations are caught in code review and must be fixed before merge.

To verify your own work: search the file you just wrote for `#` followed by three or six hex digits, and for `--palette-`. If you find either outside a `themes/` file, fix it before committing.

---

## File Responsibilities

```
assets/scss/
├── main.scss             # @use imports only. No rules. No variables. No properties.
├── _tokens.scss          # Comment-only contract. Lists every valid --color-* token name.
├── _layout-vars.scss     # SCSS $variables for breakpoints, spacing, z-index, border-radii.
├── themes/
│   ├── _catppuccin-mocha.scss   # Hex values → --palette-* under :root
│   ├── _catppuccin-latte.scss   # Hex values → --palette-* under :root (light palette)
│   ├── _theme-dark.scss         # --palette-* → --color-* under :root, [data-theme="dark"]
│   └── _theme-light.scss        # --palette-* → --color-* under [data-theme="light"]
├── _reset.scss           # CSS reset. References --color-* only.
├── _typography.scss      # Font stacks, sizes, line-heights. References --color-* only.
├── _layout.scss          # Header, footer, main shell, skip-to-content link.
├── _landing.scss         # Root landing page user grid.
├── _user-landing.scss    # Per-user hub page layout.
├── _blog.scss            # Blog list and post pages.
├── _tags.scss            # Tag pills and term pages.
├── _gallery.scss         # Gallery grid and carousel.
├── _quotes.scss          # Rotating quotes widget.
└── shortcodes/
    ├── _callouts.scss    # note, tip, warning, important, caution shortcodes.
    ├── _resume.scss      # resume-role, resume-org, profile-intro shortcodes.
    └── _profile-intro.scss
```

If your change does not fit cleanly into one of these files, that is a signal to reconsider the change — not to create a new file. If a new file is genuinely warranted, document it in `docs/architecture/decisions.md` before creating it.

---

## Writing Palette Files

A palette file has exactly one job: map hex values to `--palette-*` custom property names under `:root`. It contains nothing else.

```scss
// assets/scss/themes/_catppuccin-mocha.scss
// DO: hex values assigned to --palette-* names
// DO NOT: any selectors other than :root
// DO NOT: any --color-* properties
// DO NOT: any SCSS variables or mixins
// DO NOT: any @use statements

:root {
  --palette-base:     #1e1e2e;
  --palette-mantle:   #181825;
  // ... all palette tokens

  // Tag color pool — 10 slots assigned from palette accents
  --palette-tag-1:  var(--palette-mauve);
  --palette-tag-2:  var(--palette-blue);
  --palette-tag-3:  var(--palette-green);
  --palette-tag-4:  var(--palette-peach);
  --palette-tag-5:  var(--palette-pink);
  --palette-tag-6:  var(--palette-teal);
  --palette-tag-7:  var(--palette-yellow);
  --palette-tag-8:  var(--palette-maroon);
  --palette-tag-9:  var(--palette-lavender);
  --palette-tag-10: var(--palette-sky);
}
```

When creating a new palette (e.g., Nord), use the same `--palette-*` property names. The names are fixed — they describe the *role* within a palette (base, surface, accent colors), not the specific hue. Map the new palette's colors to these names as best fits. Document any semantic mismatches in a comment.

---

## Writing Theme Mapping Files

A theme mapping file maps `--palette-*` to `--color-*` under the correct selector. It must define every token listed in `_tokens.scss` — no gaps.

```scss
// assets/scss/themes/_theme-dark.scss
:root,
[data-theme="dark"] {
  --color-bg:               var(--palette-base);
  --color-bg-raised:        var(--palette-surface0);
  --color-bg-sunken:        var(--palette-mantle);
  --color-border:           var(--palette-surface1);
  --color-border-subtle:    var(--palette-surface0);
  --color-text:             var(--palette-text);
  --color-text-muted:       var(--palette-subtext0);
  --color-text-faint:       var(--palette-overlay1);
  --color-heading:          var(--palette-lavender);
  --color-link:             var(--palette-blue);
  --color-link-hover:       var(--palette-sapphire);
  --color-accent:           var(--palette-mauve);
  --color-accent-alt:       var(--palette-pink);
  --color-code-bg:          var(--palette-mantle);
  --color-code-text:        var(--palette-green);
  --color-callout-note:     var(--palette-blue);
  --color-callout-tip:      var(--palette-green);
  --color-callout-warning:  var(--palette-yellow);
  --color-callout-caution:  var(--palette-red);
  --color-callout-important: var(--palette-mauve);
  --color-tag-1:            var(--palette-tag-1);
  --color-tag-2:            var(--palette-tag-2);
  --color-tag-3:            var(--palette-tag-3);
  --color-tag-4:            var(--palette-tag-4);
  --color-tag-5:            var(--palette-tag-5);
  --color-tag-6:            var(--palette-tag-6);
  --color-tag-7:            var(--palette-tag-7);
  --color-tag-8:            var(--palette-tag-8);
  --color-tag-9:            var(--palette-tag-9);
  --color-tag-10:           var(--palette-tag-10);
}
```

If you add a new `--color-*` token, you must: add it to `_tokens.scss`, define it in `_theme-dark.scss`, and define it in `_theme-light.scss`. All three, always, atomically in the same commit.

---

## Writing Component SCSS Files

### Property ordering within a rule

Order CSS properties consistently so diffs are easier to read:

1. Positioning (`position`, `top`, `left`, `z-index`)
2. Display and box model (`display`, `width`, `height`, `padding`, `margin`, `border`, `border-radius`)
3. Typography (`font-*`, `line-height`, `text-*`, `color`)
4. Visual (`background`, `box-shadow`, `opacity`, `outline`)
5. Transitions and animation (`transition`, `animation`)
6. Media queries (inside the rule, at the bottom)

### Breakpoints

Always use the `$bp-*` SCSS variables from `_layout-vars.scss`. Never write pixel values in media queries directly.

```scss
// Wrong
@media (max-width: 768px) { ... }

// Right
@use 'layout-vars' as *;
@media (max-width: $bp-tablet) { ... }
```

Desktop-first: write the base rule for desktop, then add `max-width` overrides for tablet and mobile.

### Selectors

- Use BEM-ish naming for component blocks: `.blog-card`, `.blog-card__title`, `.blog-card--featured`.
- Never use ID selectors in component styles. IDs are only acceptable in `_layout.scss` for landmark elements (`#main-content`).
- Never use `!important`. If you feel you need it, the specificity problem is elsewhere — fix that instead.
- Avoid nesting more than two levels deep. Deep nesting creates high-specificity selectors that are hard to override and signal that a component is poorly decomposed.

```scss
// Acceptable — two levels
.blog-card {
  padding: 1.5rem;

  &__title {
    color: var(--color-heading);
  }
}

// Not acceptable — too deep
.blog-card {
  .content {
    .meta {
      .date { ... }  // This is four levels deep
    }
  }
}
```

### Typography

- Font sizes use `rem`, with `1rem = 16px` as the browser default.
- Headings that scale with viewport use `clamp(min, preferred, max)`.
- Body text and UI elements use fixed `rem` values.

```scss
// Scaling heading
.page-title {
  font-size: clamp(2rem, 5vw, 4rem);
}

// Fixed body
.blog-card__summary {
  font-size: 0.95rem;
  line-height: 1.6;
}
```

### No Inline Styles in Templates

The `style=""` attribute is banned in Hugo templates with one documented exception: when Hugo requires inline dimensions for image processing output (e.g., `object-position`), document the exception with a comment directly on the element.

```html
{{/* Exception: Hugo image processing requires inline object-position for focal point */}}
<img src="{{ .image }}" style="object-position: {{ .focalPoint }};" alt="{{ .alt }}">
```

### Transitions

Theme transitions (dark ↔ light) must not produce a flash. The correct approach is to transition `background-color` and `color` on `:root` with a short duration:

```scss
// In _layout.scss
:root {
  transition:
    background-color 200ms ease,
    color 200ms ease;
}
```

Do not apply `transition: all` anywhere. It causes unintended transitions on layout properties during page load.

---

## Tag Pill Color Assignment

The tag pill partial assigns a color index by hashing the tag name. The SCSS handles the color application via numbered modifier classes:

```scss
// In _tags.scss
@for $i from 1 through 10 {
  .tag-pill--#{$i} {
    $color: var(--color-tag-#{$i});
    color: $color;
    border: 1px solid $color;
    background-color: color-mix(in srgb, $color 18%, transparent);
  }
}
```

This loop generates `.tag-pill--1` through `.tag-pill--10`. The tag pill partial sets the class. Swapping a palette automatically recolors all pills — no changes to `_tags.scss` are ever needed for a palette swap.

---

## Swapping a Color Scheme

The complete procedure (all five steps are required):

1. Create `assets/scss/themes/_{palette-name}.scss` with raw hex values assigned to `--palette-*` names. Every name in the existing palette files must be present.
2. Update `assets/scss/themes/_theme-dark.scss` or `_theme-light.scss` to `@use` the new palette file instead of the old one.
3. Update `main.scss` to import the new palette file and remove the old one.
4. Update `hugo.yaml` `chroma_style_dark` or `chroma_style_light` to the nearest matching Chroma style name (run `hugo gen chromastyles --help` to list available styles).
5. Run `make build` and verify zero build errors. Run `make screenshot-test` to produce diff images for human review.

Zero component files change during a palette swap. If you find yourself editing `_blog.scss` or `_tags.scss` to accommodate a new palette, stop — something is wrong with the token mapping.

---

## Formatting and Linting

Two tools govern SCSS quality. They are complementary — Prettier handles formatting, Stylelint handles correctness.

### Prettier (formatting)

Prettier auto-formats SCSS: indentation, spacing around operators, brace placement, and property value alignment. It does not reorder properties — property ordering is a style convention enforced by code review, not a tool.

```bash
make format-scss    # auto-fix in place
make lint-scss      # check only, exits non-zero on violations
```

Prettier is configured in `.prettierrc.yaml`. YAML files are excluded from Prettier via `.prettierignore` — do not add YAML handling to Prettier.

After running `make format-scss`, your SCSS will have:
- 2-space indentation
- A space before every opening `{`
- A newline after every `}`
- No trailing whitespace
- Properties on their own lines (never collapsed to one line)

### Stylelint (correctness)

Stylelint enforces the rules that Prettier cannot — specifically the three-namespace color rule and the structural constraints that protect the theme architecture.

```bash
make lint-scss   # runs both Prettier check and Stylelint
```

Stylelint is configured in `.stylelintrc.yaml`. The key enforced rules are:

| Rule | What it catches |
|---|---|
| `color-no-hex` | Hex values outside `themes/` — the most common architecture violation |
| `custom-property-pattern` | `--custom-props` that don't match `--color-*` or `--palette-*` |
| `declaration-no-important` | Any `!important` anywhere |
| `max-nesting-depth: 2` | Selectors nested more than 2 levels deep |
| `selector-id-pattern: ^$` | ID selectors in component files |

The `color-no-hex` and `custom-property-pattern` rules are **disabled** in `assets/scss/themes/` files via the `overrides` section in `.stylelintrc.yaml`. This is intentional and must not be changed — palette files are the one legitimate home for hex values.

**When Stylelint reports a violation:** Fix the SCSS. Do not add the violation to the ignore list or disable the rule. The only exception is a new palette file, where the override in `.stylelintrc.yaml` must be extended to include the new file path.

### Property ordering (style convention, not tool-enforced)

This ordering is enforced by code review and janitor audits, not by a linter. Write properties in this order within every rule:

1. `position`, `top`, `right`, `bottom`, `left`, `z-index`
2. `display`, `flex-*`, `grid-*`, `align-*`, `justify-*`, `gap`
3. `width`, `min-width`, `max-width`, `height`, `min-height`, `max-height`
4. `padding`, `margin`
5. `border`, `border-*`, `border-radius`, `outline`
6. `font-*`, `line-height`, `letter-spacing`, `text-*`, `white-space`
7. `color`
8. `background`, `background-*`
9. `box-shadow`, `opacity`, `visibility`, `overflow`
10. `transition`, `animation`
11. Media queries (at the bottom of the rule, not at file level)

---

*This file was last updated to match `docs/product/spec.md` version 1.0.*
