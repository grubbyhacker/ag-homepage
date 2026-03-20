# Hugo Conventions

> **Location in repo:** `.agent/hugo-conventions.md`  
> **Read this:** Before creating or editing any file in `layouts/`, `archetypes/`, or `hugo.yaml`.  
> **Also read:** `.agent/agents.md` first, unconditionally.

---

## The Hugo Lookup Order Is Your Architecture

Hugo resolves templates by walking a lookup order. Understanding it prevents both over-engineering (writing per-user layouts that aren't needed) and under-engineering (missing that a fallback is picking up the wrong template).

**For a page at `/alice/blog/2025/my-post/`:**

Hugo looks for a single template in this order (first match wins):

1. `layouts/alice/blog/single.html`
2. `layouts/alice/single.html`
3. `layouts/blog/single.html`
4. `layouts/_default/single.html`

**Implication:** Do not create `layouts/{username}/single.html` unless that user genuinely needs behavior that cannot be expressed in the `_default` template with data from `site.Data.users.{username}.profile`. Most pages should use `_default` templates parameterized by user data — not per-user template copies.

**For a list page at `/alice/blog/`:**

1. `layouts/alice/blog/list.html`
2. `layouts/alice/list.html`
3. `layouts/blog/list.html`
4. `layouts/_default/list.html`

**For the root landing page at `/`:**

1. `layouts/index.html` ← this is the one to use

**For taxonomy term pages at `/tags/linux/`:**

1. `layouts/tags/term.html`
2. `layouts/_default/term.html`

---

## Template Authoring Rules

### Variables and Context

- The page context is always `.` inside a template. Pass it to partials explicitly.
- Use `$` to refer to the root context inside `range` or `with` blocks where `.` has been rebound.
- Declare variables with `:=` and assign with `=`. Never use a variable before declaring it.
- Use `with` for optional fields: `{{- with .Params.summary }}{{ . }}{{ end }}` renders nothing (cleanly) if `summary` is absent. Never use `if` + `isset` for this — `with` is idiomatic.

```html
{{/* Good — degrades gracefully */}}
{{- with site.Data.users.alice.profile.tagline }}
  <p class="tagline">{{ . }}</p>
{{- end }}

{{/* Bad — verbose and fragile */}}
{{- if isset site.Data.users.alice.profile "tagline" }}
  <p class="tagline">{{ site.Data.users.alice.profile.tagline }}</p>
{{- end }}
```

### Iterating Users

The canonical pattern for iterating all enabled users is:

```html
{{- range $username, $userData := site.Data.users }}
  {{- with $userData.profile }}
    {{- if .enabled }}
      {{/* render this user */}}
    {{- end }}
  {{- end }}
{{- end }}
```

`$username` is the directory name (e.g., `"alice"`). `$userData.profile` is the parsed `profile.yaml`. `$userData.quotes` is the parsed `quotes.yaml`. Never hardcode a user list anywhere.

### Whitespace Control

Hugo templates emit whitespace wherever there is whitespace in the template source. Use `{{-` and `-}}` (dash variants) to trim surrounding whitespace. In general:

- Use `{{-` at the start of block-level template tags
- Use `-}}` at the end when the next thing in the output is also block-level
- Inline content (inside `<p>` tags etc.) does not need dash trimming

### Partials

- Partials live in `layouts/partials/`. Every reusable fragment is a partial.
- Pass only what the partial needs. If a partial only needs the username and a post list, do not pass the entire page context.
- Partials that return a value use `{{ return $value }}` and are called with `{{ $result := partial "my-partial.html" . }}`.
- Partials that only render (no return value) are called with `{{ partial "my-partial.html" . }}`.

The tag pill partial is the canonical example of a value-return partial:

```html
{{/* layouts/partials/tag-pill.html */}}
{{/* Call: {{ partial "tag-pill.html" (dict "tag" $tagName) }} */}}
{{- $tag := .tag -}}
{{- $index := mod (len $tag | int) 10 | add 1 -}}
<a href="/tags/{{ $tag | urlize }}/" class="tag-pill tag-pill--{{ $index }}">{{ $tag }}</a>
```

### Shortcodes

- Shortcodes live in `layouts/shortcodes/`.
- Always pipe `.Inner` through `| markdownify` unless the shortcode explicitly needs raw HTML inner content.
- Named parameters use `.Get "paramname"`. Positional parameters use `.Get 0`, `.Get 1`, etc. Prefer named parameters for anything with more than one argument.
- Shortcodes that need a default value for an optional param:

```html
{{- $title := .Get "title" | default "Note" -}}
```

- Never put logic that belongs in a template into a shortcode. Shortcodes are for content authors. Templates are for structure.

### The `baseof.html` Shell

`layouts/_default/baseof.html` is the master shell. It defines the blocks that all other templates fill:

```html
<!DOCTYPE html>
<html lang="{{ site.LanguageCode }}" data-theme="dark">
<head>
  {{- partial "head.html" . -}}
</head>
<body>
  {{- partial "header.html" . -}}
  <main id="main-content">
    {{- block "main" . }}{{- end }}
  </main>
  {{- partial "footer.html" . -}}
</body>
</html>
```

Every page template defines a `{{ define "main" }}` block. Nothing else. Do not add structural HTML to individual page templates — it belongs in `baseof.html` or the partials it calls.

### The `head.html` Partial — Critical Ordering

The ordering inside `head.html` is not cosmetic — it prevents theme flicker. The required order is:

```html
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  {{/* 1. MUST BE FIRST: theme detection script — blocks paint until data-theme is set */}}
  <script>
    (function() {
      var stored = localStorage.getItem('theme');
      var preferred = stored
        ? stored
        : (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
      document.documentElement.setAttribute('data-theme', preferred);
    })();
  </script>

  {{/* 2. Stylesheets — after the theme script so data-theme is already set */}}
  {{- $style := resources.Get "scss/main.scss" | toCSS | minify | fingerprint -}}
  <link rel="stylesheet" href="{{ $style.RelPermalink }}" integrity="{{ $style.Data.Integrity }}">

  {{/* 3. Chroma highlight stylesheets — both emitted, JS toggles media attribute */}}
  {{- $darkStyle  := site.Params.chroma_style_dark  | default "catppuccin-mocha" -}}
  {{- $lightStyle := site.Params.chroma_style_light | default "catppuccin-latte" -}}
  {{- $chromaDark  := resources.Get (printf "css/chroma-%s.css" $darkStyle)  | fingerprint -}}
  {{- $chromaLight := resources.Get (printf "css/chroma-%s.css" $lightStyle) | fingerprint -}}
  <link id="chroma-dark"  rel="stylesheet" href="{{ $chromaDark.RelPermalink }}"
        media='[data-theme="dark"]'>
  <link id="chroma-light" rel="stylesheet" href="{{ $chromaLight.RelPermalink }}"
        media='[data-theme="light"]'>

  {{/* 4. Font Awesome CDN */}}
  <link rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6/css/all.min.css">

  {{/* 5. Deferred JS — after everything, non-blocking */}}
  {{- $ui := resources.Get "js/ui.js" | minify | fingerprint -}}
  <script src="{{ $ui.RelPermalink }}" defer integrity="{{ $ui.Data.Integrity }}"></script>
  {{- $quotes := resources.Get "js/quotes.js" | minify | fingerprint -}}
  <script src="{{ $quotes.RelPermalink }}" defer integrity="{{ $quotes.Data.Integrity }}"></script>

  <title>{{ if .IsHome }}{{ site.Title }}{{ else }}{{ .Title }} | {{ site.Title }}{{ end }}</title>
  <meta name="description" content="{{ with .Description }}{{ . }}{{ else }}{{ site.Title }}{{ end }}">
</head>
```

**Never** move the inline theme script after a stylesheet. **Never** make it `defer` or `async`. This is enforced by the flicker-prevention requirement in `docs/product/spec.md §10.7`.

### Chroma Syntax Highlight CSS — How to Generate

The `head.html` partial references `css/chroma-{style}.css` files via `resources.Get`. These files must exist in `assets/css/` before Hugo can find them. They are **not** auto-generated by Hugo Pipes — you must create them explicitly.

**To generate the Chroma CSS files:**

```bash
hugo gen chromastyles --style=catppuccin-mocha > assets/css/chroma-catppuccin-mocha.css
hugo gen chromastyles --style=catppuccin-latte > assets/css/chroma-catppuccin-latte.css
```

These generated files are committed to the repository. They are static assets consumed by Hugo Pipes for fingerprinting only.

**When to regenerate:** Only when the `chroma_style_dark` or `chroma_style_light` params in `hugo.yaml` change. If a new Chroma style is selected, generate the corresponding CSS file and commit it alongside the `hugo.yaml` change.

**To list available Chroma styles:** Run `hugo gen chromastyles --list` (or check the [Chroma style gallery](https://xyproto.github.io/splash/docs/all.html)).

---

## YAML Front Matter Rules

All content front matter uses YAML delimiters (`---`). Quote all string values. See the schemas in `docs/product/spec.md §8` for the full field definitions.

```yaml
---
title: "My Blog Post"
date: "2025-03-15"
draft: false
tags:
  - "programming"
  - "linux"
summary: "A one-sentence description for list views."
---
```

Dates must be quoted strings (`"2025-03-15"`) to prevent YAML's date coercion from producing a `time.Time` value where Hugo expects a string.

---

## Hugo Configuration (`hugo.yaml`)

When adding a new configuration key, follow the exact YAML structure of the existing `hugo.yaml`. Do not introduce TOML syntax (`[section]`, `key = value`). Do not add keys that are not documented in the Hugo configuration reference or this spec. If a Hugo docs example shows TOML, translate it:

<!-- markdownlint-disable MD038 -->
| TOML | YAML equivalent |
|---|---|
| `[params]` | `params:` |
| `  key = "value"` | `key: "value"` |
| `[markup.highlight]` | `markup:` / `  highlight:` |
| `  style = "mocha"` | `    style: "mocha"` |
<!-- markdownlint-enable MD038 -->

---

## Archetypes

`archetypes/blog.md` is the template for new blog posts. It pre-fills the front matter with correct defaults:

```yaml
---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: "{{ .Date }}"
draft: true
tags: []
summary: ""
---
```

Do not add front matter fields to archetypes that are not in the schema defined in `docs/product/spec.md §8`.

---

## Common Mistakes to Avoid

**Hardcoding the base URL.** Use `relURL` or `absURL` functions, never string concatenation.

```html
{{/* Wrong */}}
<a href="/alice/blog/">Blog</a>

{{/* Right */}}
<a href="{{ "/alice/blog/" | relURL }}">Blog</a>
```

**Using `.Site` instead of `site`.** In Hugo's modern template API, `site` (lowercase, no dot) is the preferred global accessor. `.Site` still works but is considered legacy.

**Calling `markdownify` on content that is already HTML.** Only use `markdownify` on strings that are markdown source. Passing HTML through `markdownify` can produce double-escaped output.

**Forgetting `| safeHTML` on trusted HTML strings.** If a template variable contains a trusted HTML string (e.g., a social icon snippet built from data), pipe it through `| safeHTML` or Hugo will escape it.

**Using `printf` for URL construction.** Use `path.Join` or Hugo's URL functions instead of string formatting.

**Creating per-user layout files unnecessarily.** If the template logic is identical across users and only the data differs, use `_default` templates that read from `site.Data.users`. Per-user layout files are only justified when the page structure genuinely differs.

---

## Template Formatting — djlint and the Style Guide

### How djlint is used here

djlint formats Hugo templates by treating `{{ }}` expressions as opaque tokens and reformatting the surrounding HTML structure. It handles indentation, attribute layout, and blank lines between blocks. It does **not** reorder attributes, does **not** rewrite template expressions, and does **not** touch whitespace that has been explicitly controlled with `{{-` / `-}}`.

Run it via:

```bash
make format-templates   # auto-fix in place
make lint-templates     # check only, exits non-zero on violations
```

djlint is configured in `.djlintrc` at the repo root. Do not modify `.djlintrc` without updating this section.

### When to suppress djlint

There are three categories of template code where djlint's output would be semantically wrong. In these cases, wrap the affected lines with suppress comments and explain why:

```html
{# djlint:off #}
{{- range $i, $item := .items -}}{{ $item.title }}{{- end -}}
{# djlint:on #}
{{/* djlint suppressed: dash-trimming on this range is load-bearing for inline rendering */}}
```

**Category 1 — Inline content with dash-trimmed expressions:**  
Any template expression inside a `<p>`, `<a>`, `<span>`, or other inline element where whitespace between words would be visible. djlint may add indentation inside inline elements that becomes a literal space in rendered output.

```html
{# djlint:off #}
<p>Written by <a href="/{{ .username }}/">{{- .display_name -}}</a> on {{ .date }}</p>
{# djlint:on #}
{{/* djlint suppressed: inline content — added indentation becomes visible whitespace */}}
```

**Category 2 — `<pre>` and `<code>` blocks:**  
djlint will indent the contents of pre-formatted blocks according to template indentation depth. That indentation appears literally in the rendered HTML. Never let djlint touch the interior of `<pre>` or `<code>` blocks.

```html
{# djlint:off #}
<pre><code class="language-{{ .lang }}">{{ .Inner }}</code></pre>
{# djlint:on #}
{{/* djlint suppressed: pre/code content must not be indented */}}
```

**Category 3 — Shortcodes with markdown `.Inner`:**  
In shortcode files where `.Inner | markdownify` is used, the template structure must not add blank lines or indentation inside the block — markdownify is sensitive to leading whitespace and blank lines when processing list items and code blocks.

```html
{# djlint:off #}
<div class="callout callout--{{ $variant }}">{{ .Inner | markdownify }}</div>
{# djlint:on #}
{{/* djlint suppressed: markdownify is whitespace-sensitive; no reformatting inside this div */}}
```

Suppressions are reviewed during janitor audits. An accumulation of suppressions in the same file is a signal that the file should be restructured, not that more suppressions should be added.

---

### Hugo Template Style Guide

This style guide covers what djlint does not enforce — naming, structure, and the conventions that make templates readable across agents and human reviewers. These rules apply to all files in `layouts/`.

#### Indentation and line length

- 2-space indentation throughout. Tabs never.
- HTML structure is indented by nesting level — a `<div>` inside a `<section>` is indented 2 more spaces.
- Template block tags (`{{- define -}}`, `{{- block -}}`, `{{- range -}}`, `{{- if -}}`) are indented at the level of their surrounding HTML, with their content indented 2 more spaces inside them.
- Maximum line length is 120 characters. Attribute lists that exceed this are split to one attribute per line, with the closing `>` on its own line.

```html
{{/* Short — fits on one line */}}
<a href="{{ $url }}" class="nav-link" aria-label="{{ $label }}">{{ $text }}</a>

{{/* Long — split to one attribute per line */}}
<a
  href="{{ $url }}"
  class="nav-link nav-link--active"
  aria-label="{{ $label }}"
  data-username="{{ $username }}"
>
  {{ $text }}
</a>
```

#### Template tag spacing

- One space inside every `{{ }}` expression: `{{ .Title }}` not `{{.Title}}`.
- Dash variants follow the same rule: `{{- .Title -}}` not `{{-.Title-}}`.
- A blank line before and after every block-level template construct (`range`, `with`, `if`, `define`, `block`) when the surrounding context is also block-level HTML.

```html
{{/* Good — blank lines around block constructs */}}
<nav class="site-nav">

  {{- range $username, $u := site.Data.users }}
    {{- with $u.profile }}
      {{- if .enabled }}
        <a href="/{{ $username }}/" class="nav-link">{{ .short_name }}</a>
      {{- end }}
    {{- end }}
  {{- end }}

</nav>

{{/* Bad — no breathing room */}}
<nav class="site-nav">
{{- range $username, $u := site.Data.users }}{{- with $u.profile }}{{- if .enabled }}<a href="/{{ $username }}/" class="nav-link">{{ .short_name }}</a>{{- end }}{{- end }}{{- end }}
</nav>
```

#### Comments

- Use `{{/* */}}` for template comments. These do not appear in rendered output.
- Use HTML `<!-- -->` only for comments that are intentionally visible to users inspecting page source. This is rare — most comments belong in template comments.
- Every partial file starts with a comment block describing its purpose, inputs, and any non-obvious behavior:

```html
{{/*
  partials/tag-pill.html

  Renders a single tag as a colored pill badge.

  Input dict:
    .tag  — string, the tag name (e.g., "programming")

  Output:
    <a> element linking to /tags/{tag}/ with color class tag-pill--{1-10}
    Color index is determined by len($tag) mod 10, giving stable color assignment.
*/}}
```

#### Attribute ordering on HTML elements

Attributes are written in this order, consistently across all templates:

1. `id` (if present)
2. `class`
3. `href` / `src` / `action` (the primary functional attribute)
4. `type` (for inputs and buttons)
5. `name` / `for` / `rel`
6. `aria-*` attributes
7. `data-*` attributes
8. All other attributes alphabetically

```html
{{/* Correct ordering */}}
<a id="site-logo" class="header__logo" href="{{ "/" | relURL }}" aria-label="Home">
  {{ site.Title }}
</a>
```

#### Variable naming in templates

- Use `$camelCase` for template variables. Hugo template variables are always prefixed with `$`.
- Loop variables follow the pattern `$username`, `$userData` (noun describing what the variable holds, not `$i`, `$v`, or `$x`).
- Boolean variables are prefixed `$is` or `$has`: `$isActive`, `$hasGallery`.

```html
{{/* Good */}}
{{- $profileData := site.Data.users.alice.profile -}}
{{- $isEnabled := $profileData.enabled -}}
{{- $hasGallery := $profileData.features.gallery | default false -}}

{{/* Bad */}}
{{- $p := site.Data.users.alice.profile -}}
{{- $e := $p.enabled -}}
```

---

*This file was last updated to match `docs/product/spec.md` version 1.0.*
