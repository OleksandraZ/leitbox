# 5. Architecture

The layers and which layer may use which. Arrows mean "imports / calls". Grey dashed parts come
after the MVP.

```mermaid
flowchart TD
    Main["__main__.py: start"]
    CFG["config.py"]
    CLI["cli: menus, input, print"]
    API["api: REST endpoints"]
    UI["web UI"]
    IMP["importers: CSV file to question/answer pairs"]
    SRV["services: ProjectService, DeckService, StudyService"]
    DOM["domain: Card, Deck, Project, User, Review, Scheduler"]
    REP["storage: UserRepository, ReviewRepository"]
    JSON["storage: JSON file"]
    DB["storage: database"]

    Main --> CFG
    Main --> CLI
    Main --> JSON
    UI --> API
    CLI --> SRV
    CLI --> IMP
    API --> SRV
    API --> IMP
    SRV --> DOM
    SRV --> REP
    JSON -. implements .-> REP
    DB -. implements .-> REP
    JSON --> DOM
    DB --> DOM

    classDef core fill:#d4edda,stroke:#2e7d32,color:#1b1b1b
    classDef afterMvp fill:#f2f2f2,stroke:#9e9e9e,stroke-dasharray: 5 5,color:#555
    class DOM core
    class API,UI,DB afterMvp
    linkStyle default stroke:#8a8a8a,stroke-width:1.5px
```

## Layers

| Layer | Package | Job | May import |
|---|---|---|---|
| **Domain** | `domain/` | Entities and Leitner rules ([domain model](04-class-diagram.md)). No files, no `print`/`input`, no database. | nothing |
| **Services** | `services/` | Use cases. `ProjectService`: create and list projects. `DeckService`: import and delete decks. `StudyService`: due cards, next due date, answer a card (rules → save review → save user, D-010). | `domain`, `storage` interfaces |
| **Storage** | `storage/` | Interfaces `UserRepository` (`get`, `save`) and `ReviewRepository` (`add`, `list_for_user`). The JSON versions share one file in `DATA_DIR` and write it safely (temp file + replace, D-005, D-010). Converters to and from JSON. | `domain` |
| **Importers** | `importers/` | CSV file → question/answer pairs, with checks (D-008). | nothing |
| **CLI** | `cli/` | Menu, one function per option. Calls the services and the importer. | `services`, `importers` |
| **Start** | `__main__.py` | Creates the repositories, the default user (D-007), the `Scheduler` and the services, then runs the CLI. Turns Ctrl+C/Ctrl+D and a damaged data file into short messages (N4). | everything |

**Dependency rule:** arrows point towards the domain, never away from it. The domain is tested
without files, and an API can be added next to the CLI without changing domain or services.

**Configuration** (`config.py`) is read only at the start; its values are passed in (e.g. the
intervals into the `Scheduler`).

## Later phases

- **Phase 2 (API):** `api/` calls the same services. A database is a second implementation of
  the same repository interfaces; `__main__` (or the API start) chooses which.
- **Phase 4 (web UI):** talks to the API only.
- `domain/` and `services/` stay as they are.

## Folder structure

```text
src/leitbox/
├── __main__.py     # start: assembles the app, runs the CLI
├── config.py       # settings from the environment + Leitner intervals
├── domain/         # Card, Deck, Project, User, Review, Scheduler
├── services/       # ProjectService, DeckService, StudyService
├── storage/        # repository interfaces, JSON implementation, converters
├── importers/      # CSV → question/answer pairs
└── cli/            # menu
```
Tests are in `tests/`, outside the package.
