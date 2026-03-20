# Hugo Family Site — Makefile
# All targets are designed to run inside the dev container.
# See .agent/ci-and-testing.md for full target documentation.

HUGO          := hugo
PRETTIER      := npx -y prettier
DJLINT        := djlint
STYLELINT     := npx -y stylelint
ESLINT        := npx -y eslint
YAMLLINT      := yamllint
MARKDOWNLINT  := npx -y markdownlint
LYCHEE        := lychee

SCSS_FILES    := "assets/scss/**/*.scss"
JS_FILES      := "assets/js/**/*.js"
LAYOUTS_DIR   := layouts/
PUBLIC_DIR    := public/

.PHONY: serve build clean \
        format format-templates format-scss format-js \
        lint lint-templates lint-scss lint-yaml lint-js lint-md \
        test test-ci screenshot-test update-screenshots \
        check-links \
        devcontainer-build devcontainer-shell

# ---------- Development ----------

serve:
	$(HUGO) server -D --baseURL=http://localhost:1313

build:
	git config --global --add safe.directory /workspace
	$(HUGO) --cleanDestinationDir

clean:
	rm -rf $(PUBLIC_DIR) resources/ .hugo_build.lock

# ---------- Formatting ----------

format: format-scss format-js format-templates

format-templates:
	$(DJLINT) $(LAYOUTS_DIR) --reformat --profile=jinja

format-scss:
	$(PRETTIER) --write $(SCSS_FILES)

format-js:
	$(PRETTIER) --write $(JS_FILES)

# ---------- Linting ----------

lint: lint-scss lint-js lint-templates lint-yaml lint-md

lint-templates:
	$(DJLINT) $(LAYOUTS_DIR) --check --profile=jinja

lint-scss:
	$(PRETTIER) --check $(SCSS_FILES)
	$(STYLELINT) $(SCSS_FILES)

lint-yaml:
	$(YAMLLINT) -c .yamllint.yaml .

lint-js:
	$(ESLINT) $(JS_FILES)
	$(PRETTIER) --check $(JS_FILES)

lint-md:
	$(MARKDOWNLINT) "content/**/*.md" "docs/**/*.md" ".agent/**/*.md"

# ---------- Testing ----------

test:
	docker compose run --rm playwright npx playwright test --reporter=html --pass-with-no-tests

test-ci:
	docker compose run --rm playwright npx playwright test --reporter=list --pass-with-no-tests

screenshot-test:
	docker compose run --rm playwright npx playwright test tests/specs/screenshot.spec.ts

update-screenshots:
	docker compose run --rm playwright npx playwright test tests/specs/screenshot.spec.ts --update-snapshots

# ---------- Validation ----------

check-links:
	$(LYCHEE) --offline --include-fragments $(PUBLIC_DIR)

# ---------- Dev Container ----------

devcontainer-build:
	docker compose build

devcontainer-shell:
	docker compose run --rm devcontainer
