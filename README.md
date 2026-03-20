# Family Homepage

A multi-user static website built with [Hugo](https://gohugo.io) — raw SCSS, no frameworks, no themes.

This project is an experiment in building a complete website using AI agents working from a detailed human-written specification. The agents handle all implementation — layouts, styling, content, testing — while humans provide the architecture, ground rules, and review.

## Where to look

- **`docs/product/spec.md`** — the full product specification that drives all agent work
- **`.agent/`** — instruction files that govern how agents operate in this repo
- **`docs/architecture/decisions.md`** — architectural decision records

## Getting started

Everything runs inside a dev container:

```bash
docker compose build
docker compose run --rm devcontainer
```

From inside the container: `make serve`, `make build`, `make lint`, `make test`.
