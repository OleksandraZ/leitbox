# Requirements — Leitbox

> Status: **draft** (Phase 0). Items marked *open* are not decided yet.

## 1. Problem

Learning material in question-and-answer form (foreign-language vocabulary, interview
questions, a driving-licence theory test…) is often learned all at once, the night before
it's needed. It's remembered for a day and then forgotten, because it never reaches
long-term memory.

**Leitbox** splits the material into small daily portions and schedules each card for review
at growing intervals (the Leitner box system). Cards you know are reviewed less and less
often; cards you get wrong come back sooner.

The engine is generic: any content that fits a question/answer card works. It is presented
with **German vocabulary** as the showcase, using demo decks.

## 2. Actors

| Actor | Description | From phase |
|---|---|---|
| **Learner** | Imports decks, reviews due cards, edits and adds single cards | 1 |
| **Guest** | Visitor without an account (e.g. of the hosted app): browses and reads the demo decks; must log in to copy one and study it | later (accounts) |

There is no separate admin role. The demo decks are ordinary **shared decks** owned by the
app author (see §3). No non-human actors: nothing happens without the learner acting. (Reminders would add one, see §7.)

## 3. Decks and cards — decisions so far

- **Getting cards in:** a whole deck is created by **importing a file** (CSV). Typing cards
  in one by one is not the main way in.
- **Maintaining a deck:** inside a deck, the learner can **edit** a card, **add** a single card
  and **delete** a card. Editing a card keeps its learning progress (box, due date).
  Not needed for the MVP: without it, a typo is fixed by re-importing the deck (progress is lost).
- **Sharing (designed now, built later):** each deck is **private** or **shared**. A shared
  deck can be **copied** by other learners. A copy is independent: later changes to the
  original don't affect it, and every learner keeps their own progress on their copy.
- **Demo decks** are shared decks owned by the app author.

## 4. Leitner rules (business rules)

| Box | Review interval |
|---|---|
| 1 | 1 day |
| 2 | 2 days |
| 3 | 7 days |
| 4 | 14 days |
| 5 | 30 days |

- New cards start in box 1.
- Correct answer → the card moves up one box. Wrong answer → it moves down one box.
- *To confirm in the next step (card lifecycle):* box 1 + wrong, box 5 + correct, retiring
  after 2 correct answers in box 5, bringing retired cards back, due date in calendar days,
  overdue cards, session order, no early reviews.
- The number of boxes, intervals and the retire threshold are configurable.

## 5. User stories

*Next step.*

## 6. Scope (MoSCoW)

Two levels: what's submitted for the course (deadline 2026-11-23) and the finished app, which
is completed later if needed.

| Feature | Course submission | Finished app |
|---|---|---|
| Import a deck (CSV), review due cards, Leitner scheduling | Must | Must |
| Edit / add / delete single cards | Could | Should |
| Accounts, shared decks, copying, guest browsing | Won't | Should |
| Reminders ("your cards are due") | Won't | Could |

*To be completed with the user stories.*

## 7. Open questions

- Guest: only the author's demo decks, or every shared deck? Can a guest try a review without
  an account (the hosted app is meant to be shown to visitors)?
- Copied decks: does a copy remember which deck it came from?
- Deleting a card: are its recorded reviews deleted too, or kept for statistics?
- CSV format: which columns, and what happens with invalid rows?
