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
