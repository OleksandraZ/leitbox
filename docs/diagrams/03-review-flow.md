# 3. Review flow

What happens in one study session, from choosing a deck until the learner is done. Blue steps
are done by the **learner**, green steps by the **system**.

```mermaid
flowchart TD
    Start([Start]) --> P[Choose a project]
    P --> D[Choose a deck]
    D --> Q{Any due cards left?}

    Q -- no --> M[Show: nothing due, and when the next card is due]
    M --> End([Back to the deck list])

    Q -- yes --> S[Show the next due card's question]
    S --> R[Reveal the answer]
    R --> K{Knew it?}

    K -- no --> B1[Move card to box 1, due tomorrow]
    K -- yes --> LB{In the last box?}
    LB -- yes --> RT[Retire card]
    LB -- no --> NB[Move card to next box, due today + its interval]

    B1 --> SV[Record the review and save]
    RT --> SV
    NB --> SV

    SV --> C{Continue?}
    C -- yes --> Q
    C -- no --> End

    classDef learner fill:#dbe9fb,stroke:#3b6fb6,color:#1b1b1b
    classDef system fill:#d4edda,stroke:#2e7d32,color:#1b1b1b
    class P,D,R,K,C learner
    class Q,M,S,LB,B1,RT,NB,SV system
    linkStyle default stroke:#8a8a8a,stroke-width:1.5px
```

## Explanation

**Before the first card.** The learner chooses a project and one of its decks: a session
always covers one deck. If nothing in the deck is due, the learner sees a message with the
date of the next due card and goes back to the deck list.

**For each card** (the loop):
1. The system shows the **question** of the next due card. The order is fixed: oldest due
   date first, then lower box, then import order (R8).
2. The learner **reveals the answer** and says whether they **knew it** (self-assessment, R1).
3. The system applies the Leitner rules (R3–R6), the same ones as in the
   [card lifecycle](02-card-states.md): *didn't know* → box 1, due tomorrow; *knew it* → the
   next box, due after that box's interval, or **retired** if the card was in the last box.
4. The review is **recorded** (R12) and **saved immediately**, before the next card is shown,
   so no answer is lost if the app stops (N1).
5. The learner continues or stops.

**Ending.** The session ends when no due cards are left or when the learner stops; either
way the learner is back at the deck list. Cards not reviewed stay due (R11). A learner can
also quit while a question is shown: that card wasn't answered, so it stays due as well.

**Each card at most once per session.** A card answered "didn't know" is due tomorrow, so it
doesn't come back in the same session (R16).
