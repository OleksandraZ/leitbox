# Decisions log

Short ADR-style entries about the implementation: what was decided, which options were
considered, and why. Newest at the bottom.

---

## D-001 — Local data vs sample data
**Decision:** Real user data lives in `data/` (git-ignored). Example data lives in `samples/`
(committed). The data path comes from configuration (`.env`), not from hard-coded paths.
**Options:** one folder with an ignore exception for samples · separate folders.
**Why:** Separate folders make the ignore rule one simple line, with no exception patterns,
and no risk of committing personal data.
**Consequence:** git doesn't track empty folders, so the app must create `data/` if it's missing.

## D-002 — Python version
**Decision:** Python 3.14, recorded in `.python-version` and the README.
**Options:** latest stable (3.14) · an older version (3.12/3.13) for wider compatibility.
**Why:** The hosting target (FastAPI Cloud) supports Python 3.10+ and uses the latest stable
version by default. Phase 1 uses only the standard library; pytest installs cleanly on 3.14.
**Consequence:** For deployment, FastAPI Cloud reads the version from `requires-python` in
`pyproject.toml`, so that file will be needed by Phase 3 at the latest.

## D-003 — Configuration: environment variables via python-dotenv
**Decision:** One config module is the only place that reads environment variables.
Values that differ per machine or are secret (data folder, later database URL and secret
key) come from the environment; locally they are loaded from `.env` with `python-dotenv`.
Rules of the app (box intervals, retire threshold) are constants in the same module.
Harmless settings have defaults; secrets have none and fail loudly if missing.
**Options:** plain `os.environ` with defaults (zero dependencies) · `python-dotenv`.
**Why:** `python-dotenv` is the common practice for local development and removes the need
to export variables by hand. On a server, variables come from the host; `python-dotenv`
does not override variables that are already set, so the same code works in both places.
`.env` is git-ignored; `.env.example` is committed as the template.
