# Leitbox

A flashcard app for spaced repetition, based on the **Leitner box system**. You import your
question/answer cards from a CSV file and study them deck by deck. Every card you know moves up
a box and comes back less often, and every card you forget goes back to box 1 and comes back
the next day. The app only shows you the cards that are due.

**Status:** planning done; the command-line app (MVP) is being built. See the
[roadmap](docs/roadmap.md), the [requirements](docs/requirements.md) and the
[design diagrams](docs/diagrams/README.md).

## Setup

Requires Python 3.14.

```bash
git clone https://github.com/OleksandraZ/leitbox.git
cd leitbox
python3.14 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pip install -e .
cp .env.example .env               # optional: change where data is stored
```

## Run

```bash
python -m leitbox                  # available from Phase 1
```

## Test

```bash
pytest
```
