# Requirements — Leitbox

> Status: **draft** (Phase 0). Items marked *(proposed)* are suggestions not confirmed yet;
> *open* items are listed in §9.

## 1. Problem

Learning material in question-and-answer form (foreign-language vocabulary, interview
questions, a driving-licence theory test…) is often learned all at once, the night before
it's needed. It's remembered for a day and then forgotten, because it never reaches
long-term memory.

**Leitbox** shows you only what's due, and spaces each card further apart as you learn it
(the Leitner box system). Cards you know come back less and less often; cards you forget
come back the next day.

The engine is generic: any content that fits a question/answer card works. It is presented
with **German vocabulary** as the showcase, using demo decks.

## 2. Terms

| Term | Meaning |
|---|---|
| **Project** | A topic the learner is studying (e.g. "German", "Driving licence"). Groups decks. |
| **Deck** | A set of cards, studied as a unit. Belongs to exactly one project. Created by import. |
| **Card** | One question with its answer. Belongs to one deck; has a box and a due date. |
| **Box** | A card's Leitner level, 1–5. The box decides the review interval. |
| **Due** | A card is due on any day where `today >= due date`. |
| **Retired** | A card that has been learned (see §4) and is no longer scheduled. |
| **Review** | One answer to one card: the learner's self-assessment, "knew it" or "didn't know". |

## 3. Actors

| Actor | Description | From phase |
|---|---|---|
| **Learner** | Creates projects, imports decks, studies due cards | 1 |
| **Guest** | Visitor without an account (e.g. of the hosted app): browses the **demo decks** and can study one right away; is invited to log in to keep the progress | after MVP (accounts) |

There is no admin role: **demo decks are seed data**, loaded by the developer from files in
`samples/` (e.g. with a script at deployment). Nobody can make a deck "demo" through the app.
No non-human actors: nothing happens without the learner acting.

## 4. Business rules

### Boxes and intervals (configurable)

| Box | Review interval |
|---|---|
| 1 | 1 day |
| 2 | 2 days |
| 3 | 7 days |
| 4 | 14 days |
| 5 | 30 days |

The number of boxes and the intervals live in one configuration place.

### Answering a card
- **R1** Correctness is **self-assessed**: the learner sees the question, reveals the answer and
  says "knew it" or "didn't know". The app doesn't check typed answers.
- **R2** New (imported) cards start in **box 1** and are **due on the day of import**.
- **R3** Knew it, in box 1–4 → the card moves **up one box**.
- **R4** Didn't know, in any box → the card goes **back to box 1** and is due the next day.
  Reason: a forgotten card should be relearned properly, and soon.
- **R5** Knew it, in the **last box (5)** → the card is **retired**: it's learned and no longer
  scheduled. So a card retires after 5 correct answers in a row, over at least 54 days.
- **R6** Due date = date of the review + the interval of the card's **new** box, in
  **calendar days** (time of day is ignored).

### Studying
- **R7** A study session covers **one deck** and shows only its due, non-retired cards.
- **R8** Order: **oldest due date first**; same due date → **lower box first**; still equal →
  **import order** (keeps the order predictable and testable).
- **R9** Overdue cards stay in their box and stay due until reviewed. No penalty and **no
  daily limit**: the learner decides how many cards to study. Overdue cards are marked.
- **R10** **No early reviews:** cards that aren't due are not shown in a session.
- **R11** The learner can stop at any time; cards not reviewed stay due.
- **R12** Every review is **recorded** (card, time, result, box before and after), so that
  statistics can be added later without new data.
- **R16** Each card is shown **at most once per session**: a card answered "didn't know" is
  due tomorrow, so it doesn't come back the same day.

### Projects and decks
- **R13** Every deck belongs to exactly one project.
- **R17** Deleting a deck deletes its cards; deleting a project deletes its decks and their
  cards. Both ask for confirmation first, with a warning of what will be lost.
- **R18** Reviews are kept when their card (or its deck or project) is deleted, so statistics
  don't change after the fact.
- **R14** *(after MVP)* A deck's visibility is one of three:
  - **private** — only the owner sees it (the default);
  - **shared** — anyone with the deck's **link** can see it and save a copy;
  - **demo** — listed publicly for everyone, guests included. Every demo deck is also
    shared; demo decks come only from seed data (see §3).
- **R15** *(after MVP)* Copying a shared or demo deck puts the copy into one of the learner's own
  projects. A copy is independent: changes to the original don't affect it, and progress is
  per copy.

## 5. User stories — MVP (Must)

### US-01 Create a project
As a learner, I want to create a project for each topic I study, so that my decks are
grouped by what I'm learning.
- **AC-01.1** Given I have no project called "German", when I create a project "German", then
  it appears in my list of projects.
- **AC-01.2** Given I already have a project "German", when I create another
  project "German", then it's refused with a message that the name already exists.
- **AC-01.3** Given I enter an empty name, when I create a project, then it's
  refused with a message that a name is required.

### US-02 Import a deck
As a learner, I want to import my cards from a CSV file into a project, so that I don't have
to type them in.
- **AC-02.1** Given a valid CSV file with 50 cards and a project "German", when I import it
  as deck "A1 verbs", then the project has a deck "A1 verbs" with 50 cards, all in box 1 and
  due today.
- **AC-02.2** Given a CSV file where some rows have a missing column or an empty
  question/answer, when I import it, then **nothing is imported** and I see an error that
  says what's wrong and where (e.g. the row number). Import is all or nothing.
- **AC-02.3** Given a file that doesn't exist or isn't a CSV, when I import it, then I see an
  error and nothing is imported.

### US-03 See what's due
As a learner, I want to see my projects and decks with the number of cards due today, so
that I know where to start.
- **AC-03.1** Given a deck with 12 due cards and 30 not due, when I look at my decks, then
  the deck shows 12 due.

### US-04 Study a deck
As a learner, I want to go through a deck's due cards one by one and say whether I knew the
answer, so that I review the right cards at the right time.
- **AC-04.1** Given a deck with cards due yesterday, due today and due tomorrow, when I start
  a session, then I get the ones due yesterday and today, in that order (R8), and not the
  one due tomorrow (R10).
- **AC-04.2** Given two cards due on the same day in box 1 and box 3, when I start a
  session, then the box 1 card comes first.
- **AC-04.3** Given a card, when it's shown, then I see the question first, and the answer
  only after I choose to reveal it.
- **AC-04.4** Given a session with 10 due cards, when I stop after 4, then the other 6 are
  still due.
- **AC-04.5** Given a deck with no due cards, when I start a session, then I see a message
  that nothing is due and when the next card is due.
- **AC-04.6** Given a card that's 3 days overdue, when it's shown, then it's marked as overdue.
- **AC-04.7** Given I answer a card "didn't know", when I continue the session, then that
  card doesn't appear again in this session (R16).

### US-06 Delete a deck
As a learner, I want to delete a deck, so that I can remove a wrong import or re-import a
corrected file. (Must: the MVP's typo workaround in §3 needs it.)
- **AC-06.1** Given a deck with 50 cards, when I delete it and confirm the warning, then the
  deck and its cards are gone, and their recorded reviews are kept (R18).
- **AC-06.2** Given a deck, when I choose delete and don't confirm, then nothing changes.

### US-05 Cards are scheduled by my answers
As a learner, I want each answer to move the card to the right box and schedule its next
review, so that cards I know come back less often and cards I forget come back soon.
- **AC-05.1** Given a card in box 2, when I answer "knew it", then it's in box 3 and due
  today + 7 days.
- **AC-05.2** Given a card in box 4, when I answer "didn't know", then it's in box 1 and due
  tomorrow.
- **AC-05.3** Given a card in box 1, when I answer "didn't know", then it stays in box 1 and is
  due tomorrow.
- **AC-05.4** Given a card in box 4, when I answer "knew it", then it's in box 5 and due
  today + 30 days.
- **AC-05.5** Given a card in box 5, when I answer "knew it", then it's retired and no
  longer shows up in sessions.
- **AC-05.6** Given a card in box 5, when I answer "didn't know", then it's in box 1 and due
  tomorrow.
- **AC-05.7** Given any card, when I answer it, then the review is recorded with time,
  result, box before and box after (R12).

## 6. User stories — after MVP

Not part of the MVP; designed for now, built after the MVP (see §7).

- **US-07 Cram mode:** as a learner, I want to go through a whole deck (retired cards
  included) without changing any boxes or due dates, so that I can refresh material I've
  already learned.
- **US-08 Share and copy decks:** as a learner, I want to share a deck by a link and save a
  deck someone shared with me into my own project, so that I can use ready-made decks.
- **US-09 Try it as a guest:** as a guest, I want to browse the demo decks and study one
  without an account, so that I can see what the app does before signing up. I'm then
  invited to log in to keep my progress. Minimum: **before** a guest starts studying, they
  are told that progress is not saved without logging in. Better (Should): progress made as
  a guest is kept when they log in.
- **US-10 Accounts:** as a learner, I want my own account, so that my projects and progress
  are private and available on any device.
- **US-11 Reset a deck:** as a learner, I want to send all cards of a deck back to box 1, so
  that I can learn a deck again from the start after some time. Retired cards come back too.
- **US-12 Edit / add / delete cards:** as a learner, I want to fix, add or remove single
  cards in a deck, so that I can maintain it without re-importing. Editing keeps the
  card's progress.
- **US-13 Delete a project:** as a learner, I want to delete a project with all its decks,
  so that I can remove a topic I no longer study (R17).

## 7. Scope (MoSCoW)

Two levels: the **MVP**, submitted for the course (deadline 2026-11-23), and the finished app,
which is completed after the MVP if needed.

| Feature | Stories | MVP | Finished app |
|---|---|---|---|
| Projects, import, see what's due, study, Leitner scheduling, delete a deck | US-01…06 | Must | Must |
| Edit / add / delete single cards | US-12 | Could | Should |
| Delete a project | US-13 | Won't | Could |
| Cram mode | US-07 | Won't | Could |
| Reset a deck | US-11 | Won't | Could |
| Accounts, shared decks, copying, guest browsing | US-08…10 | Won't | Should |
| Reminders ("your cards are due") | — | Won't | Could |

## 8. Non-functional requirements and constraints

| ID | Category | Requirement | From |
|---|---|---|---|
| **N1** | Reliability | No review is lost if the app crashes or the device loses power mid-session: each answer is saved before the next card is shown. | Phase 1 |
| **N2** | Correctness (time) | Due dates are **calendar dates in the learner's timezone**. A timezone change or a daylight-saving switch never moves a card's due date or makes a card due a day early or late. | Phase 1 (local date); per-user timezone after MVP (accounts) |
| **N3** | Configurability | The number of boxes and the interval per box are defined in one place in the code (the config module), not spread through it. Changing them is a developer task. | Phase 1 |
| **N4** | Usability | Error messages say what went wrong and what to do; the learner never sees a stack trace. | Phase 1 |
| **N5** | Security / robustness | An import file is refused if it's larger than **1 MB** or has more than **2,000 cards**. | Phase 1 |
| **N6** | Usability | A new visitor can try a demo deck without logging in (US-09). | after MVP (accounts) |
| **N7** | Security | Passwords are stored hashed, never in plain text. A learner can only see their own private decks. | after MVP (accounts) |
| **N8** | Maintainability | The core (Leitner rules, cards, decks) contains no input/output, file, database or web code; the CLI, API and UI call the same core. Every business rule in §4 that's part of the MVP has at least one automated test. | Phase 1 |

**Constraints:** Python 3.14 · standard library only in Phase 1 (plus `python-dotenv`) ·
pytest for tests · FastAPI for the API (Phase 2) · MVP submitted by 2026-11-23 ·
one developer, ~2-hour sessions.

**Out of scope for now:** performance targets (no realistic baseline before the MVP exists;
revisit after Phase 1), scalability (single learner until accounts exist), and changing the
Leitner rules while cards exist (N3).

## 9. Open questions

- **CSV format:** which columns (question, answer, anything else)?
- **Cram mode:** does it record reviews for statistics?
- **Shared link:** can a guest open a shared link, or only logged-in learners?
- **Copied decks:** does a copy remember which deck it came from?
