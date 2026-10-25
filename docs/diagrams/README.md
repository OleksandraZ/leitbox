# Diagrams — overview

The model of Leitbox, from *what the app does* to *how it's built*. Each diagram builds on the
previous one. All diagrams are written in [Mermaid](https://mermaid.js.org/), which GitHub
renders directly.

| # | Diagram | What it shows |
|---|---|---|
| 1 | [Use cases](01-use-cases.md) | Who uses Leitbox (learner, guest) and for which goals, marked by what's part of the MVP and what comes after it. |
| 2 | [Card lifecycle](02-card-states.md) | The states of one card (boxes 1–5, retired) and how "knew it" / "didn't know" move it between them. |
| 3 | [Review flow](03-review-flow.md) | One study session step by step: who does what, the two decisions of the Leitner rules, saving after every answer, and how the session ends. |
| 4 | [Domain model](04-class-diagram.md) | The classes of the core (user, project, deck, card, review, scheduler), their data and methods, and how they relate. *Draft.* |
| 5 | Architecture (layers) | *coming next* |
| 6 | Review session (sequence diagram) | *planned* |
| 7 | Database (ER diagram) | *planned* |
