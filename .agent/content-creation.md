# Content Creation

> **Location in repo:** `.agent/content-creation.md`  
> **Read this:** Before creating or editing any file in `content/` or `data/`.  
> **Also read:** `.agent/agents.md` first, unconditionally.

---

## Why Content Matters Here

This site is a demonstration artifact. The example content is not decoration — it is the primary vehicle for proving that every feature works, every layout renders correctly, and every interaction behaves as specified. Agents are expected to create and maintain content with the same rigor applied to code.

"Lorem ipsum" text, placeholder titles like "Post 1", and skeleton front matter with empty fields are never acceptable. Content must be realistic, coherent, and persona-appropriate.

---

## The Six Seed Users

Every content and data task begins with these six users. Agents must maintain complete, correct content for all six at all times.

| Username | Persona | Blog focus | Gallery |
|---|---|---|---|
| `alice` | Principal software engineer. Opinionated about distributed systems, testing, and developer tooling. Dry humor. | Systems programming, distributed systems, testing, career | Photo portfolio — landscape and street photography |
| `bob` | Home baker turned amateur woodworker. Teaches himself new skills by doing. | Sourdough, woodworking projects, tool reviews, learning in public | None |
| `carol` | Retired textile artist and quilter. Precise, methodical, deeply knowledgeable about color and pattern. | Quilting technique, fabric selection, pattern analysis, show recaps | Quilt portfolio — original and traditional designs |
| `dave` | Travel photographer, semi-retired. Lived in six countries. Currently somewhere in Southeast Asia. | Photography technique, gear, travel journals, post-processing | Photo portfolio — travel and documentary |
| `eve` | Security researcher and conference speaker. Direct, technically rigorous, allergic to hype. | Vulnerability research, CTF writeups, conference talks, infosec commentary | None |
| `frank` | Retro gaming hobbyist and hardware tinkerer. Collects and restores vintage consoles. Nostalgia, but with a soldering iron. | Game reviews, console restoration, emulation, gaming history | None |

Agents may deepen any persona to make content feel more lived-in. What agents must never do is flatten personas into generic filler.

---

## Minimum Content Requirements

These are floors, not targets. More is better when more adds quality.

### Data files (must exist before any content is created)

For each of the six users, the following must exist and be complete:

- `data/users/{username}/profile.yaml` — all required fields populated; optional fields populated where relevant to the persona
- `data/users/{username}/quotes.yaml` — minimum 5 quotes; quotes must be authentic to the persona's voice and interests

### Blog posts

- Minimum **5 posts per user** (30 posts total minimum)
- Minimum **3 distinct tags per user**
- Tags must overlap across users — at least 4 tags must be used by 3 or more users, so that global tag term pages are non-trivial
- Posts must be coherent multi-paragraph articles, not outlines or summaries
- At least one post per user must use each of the following shortcodes: `note`, `tip` or `warning`, and a code block with syntax highlighting
- At least one post per user must demonstrate the `showcase` or `list-columns` shortcode
- Posts must span at least two different calendar years (to test the dated directory structure)

### About / resume pages

- Every user must have `content/{username}/about/index.md`
- Every about page must use:
  - `profile-intro` shortcode with headshot image and attribute list
  - At minimum two `resume-role` shortcodes
  - At minimum one `resume-org` shortcode
  - At minimum one callout shortcode (`note`, `tip`, `warning`, `important`, or `caution`)
- Content must be realistic — invented but plausible career histories, not placeholder text

### Gallery cards (Alice, Carol, Dave only)

- Minimum **6 cards per user** with gallery enabled
- Every card must have a complete `metadata` block appropriate to the gallery type
- Card images should be plausible paths (e.g., `/images/carol/gallery/star-trail.jpg`) even if the images do not yet exist — templates degrade gracefully on missing images
- Card front matter must be dated across at least two years

### Placeholder images

For initial implementation, use plausible file paths for all image references (`avatar`, `headshot`, gallery images) even though the actual image files do not exist yet. Templates must degrade gracefully when images are missing — use `alt` text on all `<img>` elements so the page remains readable without images. Do not reference external placeholder image services (e.g., `placeholder.com`, `picsum.photos`). When real images become available, they replace the paths with no template changes needed.

**Avatar vs. headshot:** `avatar` is the small circular image used in the landing page grid and user hub page header (96px–128px). `headshot` is the larger rectangular image used in the `profile-intro` shortcode on the about page. They are different images with different aspect ratios and crops — do not use the same file for both.

---

## Content File Structure

### Blog post

```
content/{username}/blog/{year}/{slug}/index.md
```

Example: `content/alice/blog/2024/understanding-raft/index.md`

The directory name is the slug. Use kebab-case. Keep slugs short and descriptive — 3 to 5 words. Never use dates in the slug itself (the year is already in the directory path).

### Gallery card

```
content/{username}/gallery/{slug}/index.md
```

Example: `content/carol/gallery/lone-star-medallion/index.md`

### About page

```
content/{username}/about/index.md
```

This is always `index.md` directly — no subdirectory needed.

---

## YAML Front Matter Rules

All front matter uses YAML between `---` delimiters. Quote all string values. See `docs/product/spec.md §8` for the full schemas.

```yaml
---
title: "Understanding the Raft Consensus Algorithm"
date: "2024-09-12"
draft: false
tags:
  - "distributed-systems"
  - "consensus"
  - "programming"
summary: "A practical walkthrough of leader election and log replication in Raft, with annotated Go examples."
---
```

**Common mistakes to avoid:**

- Unquoted dates (`date: 2024-09-12`) — YAML coerces these to `time.Time` objects; always quote them
- Unquoted tag values that could be misread as booleans (`no`, `yes`, `on`, `off`)
- Missing `summary` field — the blog card list will fall back to truncating the body, which rarely produces a good result

---

## Writing Conventions for Blog Posts

**Voice:** Each user has a distinct voice. Alice is precise and slightly wry. Bob is enthusiastic and self-deprecating. Carol is methodical and specific. Dave is reflective and observational. Eve is direct and technically dense. Frank is nostalgic but technically grounded. Write in that voice.

**Structure:** Most posts should have:
- An opening paragraph that establishes the problem or context
- Two to five body sections (using `##` headings)
- A closing paragraph or takeaway

**Code examples:** Use fenced code blocks with language tags. Every post that demonstrates a technical concept should have at least one code block. Choose languages appropriate to the user's persona — Alice writes Go and Python, Eve writes Python and C, Frank writes assembly and C.

**Shortcode usage:** Shortcodes exist to be used. A post about a gotcha should use `{{< warning >}}`. A post sharing a useful trick should use `{{< tip >}}`. A post on a resume page describing an overlapping role should use `{{< note >}}`. Do not use shortcodes decoratively — use them when the content genuinely calls for them.

**Internal links:** Posts may link to other posts by the same user using relative paths. Cross-user links are acceptable but should be rare and purposeful.

---

## Tag Conventions

Tags are lowercase, hyphenated, and singular where natural:

```yaml
tags:
  - "distributed-systems"   # hyphenated phrase
  - "programming"           # singular
  - "go"                    # language names are lowercase
  - "woodworking"           # compound treated as one word
```

Never use title case, spaces, or underscores in tags. Tags are also used as URL slugs by Hugo (`/tags/distributed-systems/`), so avoid anything that produces an awkward URL.

**Shared tags across users** (required overlap — agents must use these for at least two users each):

| Tag | Appropriate for |
|---|---|
| `programming` | Alice, Eve, Frank |
| `linux` | Alice, Eve |
| `photography` | Alice, Dave |
| `tools` | Alice, Bob, Frank |
| `learning` | Bob, Carol, Frank |
| `hardware` | Frank, Eve |
| `writing` | Any user |

Add more shared tags as content grows. The goal is a tag term page that shows posts from multiple authors, proving the global taxonomy works correctly.

---

## Gallery Card Conventions

### Alice and Dave — Photo portfolios

Metadata should describe the photograph:

```yaml
metadata:
  location: "Chiang Rai, Thailand"
  year: 2023
  camera: "Fujifilm X-T5"
  lens: "23mm f/2"
  technique: "Long exposure"
  description: "Dawn light over the White Temple's reflecting pool."
```

### Carol — Quilt portfolio

Metadata should describe the quilt:

```yaml
metadata:
  year_completed: "2022"
  dimensions: "60 x 72 inches"
  technique: "Hand-pieced, hand-quilted"
  materials: "Kona cotton solids, Moda Bella solids"
  pattern: "Original medallion design"
  color_story: "Deep navy and gold inspired by Islamic geometric tile work"
```

---

## Quotes File Conventions

Quotes must feel authentic to the persona. Alice quotes computer scientists and engineers. Bob quotes craftspeople, chefs, and teachers. Carol quotes designers, artists, and quilters. Dave quotes photographers and travelers. Eve quotes security researchers and skeptics. Frank quotes game designers, console pioneers, and his own childhood.

```yaml
# data/users/eve/quotes.yaml
quotes:
  - text: "Security is not a product, but a process."
    attribution: "Bruce Schneier"
  - text: "The most dangerous phrase in the language is 'we've always done it this way.'"
    attribution: "Grace Hopper"
  - text: "Complexity is the enemy of security."
    attribution: "Bruce Schneier"
  - text: "Given enough eyeballs, all bugs are shallow."
    attribution: "Eric S. Raymond"
  - text: "There are only two types of companies: those that have been hacked, and those that don't know it yet."
    attribution: "John Chambers"
```

---

## When a New Feature Is Added to the Spec

When `docs/product/spec.md` adds a new shortcode, layout feature, or data field, agents must:

1. Update at least two users' content to demonstrate the new feature in a realistic context
2. Update the relevant user's about page if the feature is relevant to resume/shortcode content
3. Verify that the new feature renders correctly for those two users before the PR is merged

The two users chosen should be from different personas and ideally have different gallery/feature configurations.

---

## Content That Agents Must Not Create

- Placeholder text (lorem ipsum, "Post Title Here", "Description goes here")
- Content that references real people in a way that could be defamatory or misleading
- Content that could be read as representing actual views of any real person named
- Content requiring images that cannot be represented as placeholder paths

---

*This file was last updated to match `docs/product/spec.md` version 1.0.*
