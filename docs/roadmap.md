# Roadmap — Leitbox

The order in which the app is built, and why. Every phase ends in a working, tested app:
the code on `main` always runs and its tests pass.

Requirements and user stories (US-xx): [requirements.md](requirements.md) · Design:
[diagrams](diagrams/README.md)

## Milestones

| Target date | Milestone | What can be shown |
|---|---|---|
| Oct 29 | Plan approved | Requirements, diagrams, folder structure, roadmap, README |
| Nov 12 | Check-in 1 | Phase 1 done: the MVP works from the command line, with tests |
| Nov 17 | Check-in 2 | Phase 2 in progress: the API works on the existing storage |
| Nov 24 | Check-in 3 + submission | Phase 2 done; Phase 3–4 as far as they got |

## Phase 0 — Requirements and design ✅

Problem, actors, Leitner rules, user stories with acceptance criteria, non-functional
requirements, scope (MVP vs. after MVP). Diagrams: use cases, card states, review flow,
class diagram, architecture. Package structure for the layers.

## Phase 1 — Core + command-line app (MVP)

**Approach:** the domain (the Leitner rules) is built first, because it's pure Python and
can be fully tested on its own. After that, the app grows in **vertical slices**: each slice
is one use case that works end to end (command line → service → domain → JSON storage), so
the app can be run and shown after every slice, and a late slice can be cut without leaving
half-built layers behind.

| # | Slice | Stories | Done when |
|---|---|---|---|
| 0 | **Config + domain:** settings module (data folder, boxes and intervals); `Card`, `Deck`, `Project`, `User`, `Review`, `Scheduler` with the Leitner rules. Only what the MVP slices need. | US-05 (rules) | Every MVP scheduling rule in requirements §4 has a passing unit test, with no files or input/output involved. |
| 1 | **Create and list projects:** first menu of the command-line app, project service, JSON storage (including converting entities to and from JSON). | US-01 | A project created in the app is still there after a restart; duplicate and empty names are refused. |
| 2 | **Import a deck:** CSV format decided, CSV importer with its checks, a committed sample CSV, deck and cards saved. | US-02 | The sample CSV imports into a project; a broken file imports nothing and says which row is wrong. |
| 3 | **See what's due:** projects and decks with the number of cards due today. | US-03 | The counts match the cards' due dates. |
| 4 | **Study a deck:** due cards in order, question then answer, "knew it" / "didn't know", boxes and due dates updated, every review recorded and saved immediately. | US-04, US-05 | A full session works from the command line and survives quitting halfway. |
| — | **MVP scope review:** with the basics working, decide whether small extras (e.g. rename a project) still fit. | — | Decision recorded. |
| 5 | **Delete a deck:** with confirmation; reviews are kept. | US-06 | The deck and its cards are gone, the reviews are still stored. |
| 6 | **Finish:** error-handling pass (no stack traces for the learner), README complete. | — | All MVP acceptance criteria pass; tagged `phase-1`. |

## Phase 2 — REST API + database

The detailed slices are planned once Phase 1 works. Decided so far:

- **Database choice first** (SQLite or TinyDB), after checking how the hosting platform keeps
  stored data between deploys. The choice is recorded in [decisions.md](decisions.md).
- **API before database.** The FastAPI endpoints call the same services as the command-line
  app, still using the JSON storage. Then the database comes in as a second implementation of
  the same storage interface, without changes to the API, the services or the domain. This
  order gives a working API early, and it proves that the storage is swappable.
- Open question: should API responses use the same shape as the stored data, or their own?

## Phase 3 — Deploy

The API hosted online (FastAPI Cloud or an alternative). Planned once Phase 2 works.

## Phase 4 — Web UI

A simple web page for studying a deck, talking to the API only. Planned once Phase 2 works.

Phases 3 and 4 may continue after the course submission: the goal is a finished, hosted app.
