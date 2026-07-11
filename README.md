# Movie Night Picker

A group decision-making app that ends the eternal "what should we watch tonight" debate, combining real-time group voting with a smart set-builder that fits your picks into the time you actually have.

## The Problem

Picking movies as a group usually means endless scrolling, decision fatigue, and a plan that blows way past everyone's bedtime. Movie Night Picker fixes both halves of that: it helps the group actually agree on something, and it makes sure whatever gets picked fits the time available.

## How It Works

- **Vote together, live.** Start or join a session and vote on movies in real time with the group.
- **Build a set, not just a pick.** The set-builder tracks each movie's duration and remaining "slack" in the session, greying out selections that would blow the time budget as you build your lineup.
- **Swipe-based onboarding.** Swipe through movies early on to help the app learn your taste (taste-based recommendations planned).
- **Save and reuse.** Save sets you've built for future movie nights.

## Repository Structure

```
movie-night-app/
├── frontend/                 # React + TypeScript + Tailwind - Yasitha
│   ├── src/
│   │   ├── components/
│   │   │   ├── MovieCard/
│   │   │   ├── Calculator/
│   │   │   ├── SessionRoom/
│   │   │   ├── VotingScreen/
│   │   │   └── GreyoutTimeline/     # consumes SetBuilder's active/slack state
│   │   ├── pages/
│   │   ├── hooks/                    # useSocket, useSession, useSetBuilder
│   │   ├── api/
│   │   └── styles/
│   └── package.json
│
├── realtime-service/         # Node + Express + Socket.io — Janitha
│   ├── src/
│   │   ├── sockets/            # vote events, session events
│   │   ├── routes/
│   │   ├── models/
│   │   └── controllers/
│   └── package.json
│
├── data-service/              # Python + FastAPI — Rehan
│   ├── app/
│   │   ├── core/                 # SetBuilder logic
│   │   │   ├── Node.py             # movie node: duration, slack, active, selected
│   │   │   ├── MergeSort.py        # sorts nodes by index
│   │   │   └── SetBuilder.py       # runtime-constraint logic (select/deselect, active flags)
│   │   ├── routers/
│   │   │   ├── calculator.py
│   │   │   ├── saved_sets.py
│   │   │   ├── set_builder.py       # API layer wrapping SetBuilder for the greyout feature
│   │   │   ├── swipe_onboarding.py
│   │   │   └── taste_learning.py    # later
│   │   ├── services/               # TMDB integration + caching
│   │   ├── db/
│   │   └── models/                  # Pydantic schemas
│   └── requirements.txt
│
├── shared/
│   └── contracts.md            # API contracts between services — Senal
│
└── docs/
    └── figma-exports/
```

## Tech Stack

**Frontend**
- React + TypeScript + Tailwind

**Backend — dual-service architecture**
- `realtime-service` — Node.js, Express, Socket.io — handles live session and voting events
- `data-service` — Python, FastAPI — handles movie data (TMDB integration), the set-builder/greyout logic, saved sets, and swipe onboarding

**Integration**
- Shared API contracts (`shared/contracts.md`) define how the frontend and both backend services talk to each other, including the set-builder's select/deselect contract

## Architecture

```
┌──────────────────┐      ┌────────────────────┐
│                  │─────▶│ realtime-service  │  (Node/Express/Socket.io)
│  React Frontend  │      │ sessions, voting   │
│                  │◀─────│                   │
│                  │      └────────────────────┘
│                  │
│                  │      ┌──────────────────────┐
│                  │─────▶│   data-service       │  (FastAPI)
│                  │      │  movies, set-builder,│
│                  │◀─────│  saved sets, TMDB    │
└──────────────────┘      └──────────────────────┘
```

## Team

- **Senal** — API contract design, cross-service integration, future mobile port
- **Rehan** — `data-service` core (SetBuilder, Node, MergeSort)
- **Janitha** — `realtime-service` (sockets, session/vote events)
- **Yasitha** - Frontend + designing

## Roadmap

- [ ] Core voting + session flow
- [ ] Set-builder / greyout timeline
- [ ] Swipe-based onboarding
- [ ] Saved sets
- [ ] Taste learning
- [ ] Native mobile port

## Getting Started

> Setup instructions coming soon — will be added once each service's entry point is finalized.

## License

TBD
