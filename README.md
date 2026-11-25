# Leitbox

A command-line flashcard app based on the Leitner box system.

**Status:** Phase 1 (CLI MVP) is complete. Next: REST API. See the [roadmap](docs/roadmap.md),
[requirements](docs/requirements.md) and [diagrams](docs/diagrams/README.md).

## Setup

Requires Python 3.14.

```bash
git clone https://github.com/OleksandraZ/leitbox.git
cd leitbox
python3.14 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pip install -e .
cp .env.example .env               # optional
```

## Run

```bash
python -m leitbox
```

Menu: `1` create a project · `2` list projects and due cards · `3` import a deck ·
`4` study a deck · `5` delete a deck · `0` quit.

Quick start: create project `German` → import `samples/german-a1-verbs.csv` as deck `A1 verbs`
→ study `German` / `A1 verbs`.

## CSV format

```csv
question,answer
sein,to be
gehen,"to go, to walk"
```

UTF-8, `.csv`, header with `question` and `answer`. Max 2,000 cards and 1 MB.
Full rules: [requirements R20](docs/requirements.md).

## Leitner rules

- Boxes 1–5, intervals 1 / 2 / 7 / 14 / 30 days (`src/leitbox/config.py`).
- Knew it → next box. Didn't know → box 1, due tomorrow. Knew it in box 5 → retired.

## Data

Stored in `data/leitbox.json`. Change the folder with `DATA_DIR` in `.env`.

## Test

```bash
pytest
```
