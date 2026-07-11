# 🎬 NewWorld
A full-stack collaborative movie discovery and watch-planning platform with live sessions, realtime voting runtime-aware filtering, and shared movie sets.
<br>

## Features
- Movie filtering and sorting
- Runtime-aware movie set builder
- Saved movie sets
- Live voting and ratings
- Collaborative watch planning
- **TMDB API** integration
<br>

## 🛠️ Tech Stack
### **Frontend**
- React
- Vite
- JavaScript/TypeScript
- TailwindCSS/CSS3
- GSAP

### Backend
- Node.js
- Express.js
- Socket.IO
- FastAPI

### Database
- [Undecided]
<br>

## 📁 Repository Structure
```
movie-night-app/
├── frontend/                 # React + TypeScript + Tailwind
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
├── realtime-service/         # Node + Express + Socket.io — jani
│   ├── src/
│   │   ├── sockets/            # vote events, session events
│   │   ├── routes/
│   │   ├── models/
│   │   └── controllers/
│   └── package.json
│
├── data-service/              # Python + FastAPI — reh
│   ├── app/
│   │   ├── core/                 # ← reh's actual commit lives here
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
│   └── contracts.md            # Lamar owns — includes SetBuilder's select/deselect contract
│
└── docs/
    └── figma-exports/
```

## 💻 Getting Started
<br>

## 📜 License
Source code is licensed under [**MIT License**](https://opensource.org/license/mit).
