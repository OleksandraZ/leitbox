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
Rules of the app (number of boxes, box intervals) are constants in the same module.
Harmless settings have defaults; secrets have none and fail loudly if missing.
**Options:** plain `os.environ` with defaults (zero dependencies) · `python-dotenv`.
**Why:** `python-dotenv` is the common practice for local development and removes the need
to export variables by hand. On a server, variables come from the host; `python-dotenv`
does not override variables that are already set, so the same code works in both places.
`.env` is git-ignored; `.env.example` is committed as the template.

## D-004 — Time and user passed into the scheduler
**Decision:** `Scheduler.answer(card, knew_it, now, user_id)`. `now` is a timezone-aware
`datetime` from the caller; the due date uses `now.date()` and the review stores `now`. The
review gets the user's ID from the caller (the single default user in the MVP).
**Options:** pass `today` and `now` separately · let the service create the review · leave
`user_id` off reviews until accounts exist.
**Why:** One `now` can't disagree with itself, and the core still never reads the clock, so
tests choose the time. With `user_id` set from the start, reviews already have an owner when
accounts come (and still after their card is deleted, R18), so nothing stored has to change.

## D-005 — JSON storage: one nested file, one repository per aggregate
**Decision:** Phase 1 stores everything in one file, `DATA_DIR/leitbox.json`. Each user is
stored with its projects, decks and cards nested inside, the same shape as the domain
classes. Reviews will be a separate list in the same file (slice 4), because they must outlive
their cards (R18). The storage interface is a `UserRepository` with `get(user_id)` and
`save(user)`; the JSON implementation reads and rewrites the whole file. Converting objects
to and from dicts lives in `storage/`, not in the domain.
**Options:** one nested file · one file per entity (projects, decks, cards, reviews as flat
lists linked by IDs, like database tables).
**Why:** The nested shape needs no extra ID fields on `Deck` or `Card` and no code to rebuild
the tree on load, so slice 1 stays small. Rewriting the whole file is fine at this size (one
learner, N5 caps a deck at 2,000 cards). The database in Phase 2 is a second implementation of
the same interface; it will use tables with foreign keys internally.
**Consequence:** Every save rewrites the file, so a crash during a write could damage it. This
matters for N1 and is handled in slice 4 at the latest (write to a temporary file, then
replace).

## D-006 — Project name rules live in the domain
**Decision:** A `Project` refuses an empty name when it's created; `User.add_project` refuses
a name the user already has. Both raise `ValueError`. Names are trimmed (spaces at the ends
are removed) and compared ignoring upper/lower case, so " german" is a duplicate of "German".
The trimmed name is stored as typed.
**Options:** checks in the service · exact or case-sensitive comparison.
**Why:** The class that has the data does the check: `User` knows its projects. The rules are
testable without storage, and the API (Phase 2) gets them without repeating them. Ignoring
case avoids two projects that look the same in the list.

## D-007 — The default user: fixed ID, created at startup
**Decision:** The MVP has one learner with a fixed ID, `DEFAULT_USER_ID = "local"` in
`config.py`. On every start, `__main__.py` loads that user from storage and, if it isn't
there yet (first start), creates and saves it. Services receive the user's ID and assume the
user exists.
**Options:** a random ID created on the first start and remembered in the data file · the
service creates the user when it's missing.
**Why:** A fixed ID needs no extra storage, and restarts always find the same user. Services
then work like they will after a login: they get the ID of a user who exists. With accounts,
the login provides the ID and the startup step goes away; services don't change.
