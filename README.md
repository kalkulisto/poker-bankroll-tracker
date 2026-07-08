# 🃏 Chico und Zwieback — Poker Bankroll Tracker

A personal poker bankroll tracker PWA built for two players, featuring cash game tracking, tournament management, head-to-head leaderboard, and a 100-tournament challenge.

**Live:** https://poker-bankroll-tracker-7mk8.onrender.com

---

## Features

### Core
- **PIN-based login** for two players (SHA256 + JWT), forced PIN change on first login
- **Cash Games** — track sessions with buy-in, cash-out, duration, stakes, location, notes
- **Tournaments** — shared calendar (global = visible to all / personal = own only)
- **Reentries** — effective buy-in calculated as `buy_in × (reentries + 1)`
- **Field size** — optional entrant count per tournament, enables Top 10% badge
- **Cascade delete** — deleting a tournament removes all associated entries automatically

### Navigation (in order)
1. **Cash Games** — list and manage cash game sessions
2. **Cash-Stats** — cumulative bankroll chart, win rate, ROI, profit/hour
3. **Turniere** — tournament calendar with filters (All / Upcoming / Registered)
4. **Turnier-Stats** — tournament stats with date range filter
5. **Rangliste** — head-to-head leaderboard (default start page)
6. **Gesamt** — combined cash + tournament view with cumulative timeline chart

### Leaderboard & Gamification
- **Head-to-Head Leaderboard** — profit, ROI, ITM rate per player
- **Head-to-Head ITM Score** — e.g. "ElChicoDe 5 : 3 XXzwiebackXX"
- **Badges** per player: 💰 ITM · 🏆 Final Table (top 9) · 🥉 Top 3 · ⭐ Top 10% · 💵 Biggest Single Win
- **Form indicator** — last 8 results as green/red dots with date + profit tooltip
- **100-Tournament Challenge** — progress bar (X/100), live lead gap, confetti milestone popups at 25/50/75/100 tournaments
- **Shared tournament detail** — placement shown as "#200 / 1742" when field size is set

### Stats & Charts
- Date range filter on both Turnier-Stats and Cash-Stats (and Gesamt)
- Cumulative timeline chart (Cash / Tournament / Total lines) with Y-axis dollar values
- Monthly bar chart for cash game development
- All stats respect reentries in profit/invested calculations

### PWA
- Installable on Android (Chrome) and iOS (Safari → Add to Home Screen)
- Service Worker with network-first strategy, API calls never cached
- Cache version bump on every frontend change forces refresh

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Database | Google Sheets (via gspread) |
| Frontend | Vanilla JS, single-file HTML PWA |
| Hosting | Render (Free tier — spins down after inactivity) |
| Auth | SHA256 PIN hash + JWT (30-day expiry) |

---

## Google Sheets Schema

All data lives in a single Google Spreadsheet. Four sheets are used (all hidden from view):

### `poker_users`
| Column | Type | Description |
|---|---|---|
| id | int | Auto-increment |
| name | string | Display name |
| pin_hash | string | SHA256 hash of PIN |
| is_admin | bool | Admin can create global tournaments and manage users |
| pin_changed | bool | False = force PIN change on next login |
| created_at | datetime | ISO timestamp |

### `poker_sessions` (Cash Games)
| Column | Type | Description |
|---|---|---|
| id | int | Auto-increment |
| user_id | int | FK → poker_users |
| date | date | YYYY-MM-DD |
| location | string | Casino / platform name |
| game_type | string | NL Hold'em / PLO |
| stakes | string | e.g. 1/2, 2/5 |
| buy_in | float | Buy-in amount ($) |
| cash_out | float | Cash-out amount ($) |
| duration_minutes | int | Session duration (optional) |
| notes | string | Optional notes |
| created_at | datetime | ISO timestamp |

### `poker_tournaments`
| Column | Type | Description |
|---|---|---|
| id | int | Auto-increment |
| name | string | Tournament name |
| series | string | e.g. WSOP, Wynn Fall Classic |
| location | string | Casino / online platform |
| start_date | date | YYYY-MM-DD |
| end_date | date | YYYY-MM-DD |
| buy_in | float | Base buy-in ($) |
| game_type | string | NL Hold'em / PLO |
| is_global | bool | Visible to all users (admin only) |
| created_by | int | FK → poker_users |
| field_size | int | Number of entrants — optional, enables Top 10% badge |
| created_at | datetime | ISO timestamp |

### `poker_entries` (Tournament Results)
| Column | Type | Description |
|---|---|---|
| id | int | Auto-increment |
| user_id | int | FK → poker_users |
| tournament_id | int | FK → poker_tournaments |
| result_position | int | Final placement |
| prize_money | float | Prize won ($) |
| reentries | int | Number of re-entries (0 = none) |
| notes | string | Optional notes |
| created_at | datetime | ISO timestamp |

> **Profit calculation:** `prize_money - (buy_in × (reentries + 1))`
>
> **Shared tournament** = same tournament_id with entries from ≥ 2 different users → appears in leaderboard

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/auth/login` | Login with name + PIN, returns JWT |
| GET | `/auth/users` | List all users (public, for login screen) |
| POST | `/auth/users` | Create user (admin only) |
| PUT | `/auth/users/{id}/pin` | Change PIN |
| GET | `/sessions/` | List own cash game sessions |
| POST | `/sessions/` | Create session |
| PUT | `/sessions/{id}` | Update session |
| DELETE | `/sessions/{id}` | Delete session |
| GET | `/tournaments/` | List visible tournaments with own entry |
| POST | `/tournaments/` | Create tournament |
| PUT | `/tournaments/{id}` | Update tournament |
| DELETE | `/tournaments/{id}` | Delete tournament + cascade entries |
| PUT | `/tournaments/{id}/entry` | Register / update result |
| DELETE | `/tournaments/{id}/entry` | Unregister |
| GET | `/stats/summary` | Cash game summary stats |
| GET | `/stats/monthly` | Monthly cash game breakdown |
| GET | `/stats/tournaments` | Tournament stats with monthly breakdown |
| GET | `/stats/combined` | Combined monthly data (cash + tournaments) |
| GET | `/stats/timeline` | Chronological events for cumulative chart |
| GET | `/stats/leaderboard` | Shared tournament leaderboard + challenge + badges |

---

## Environment Variables (Render)

| Variable | Description |
|---|---|
| `GOOGLE_CREDENTIALS` | Service account JSON (stringified) |
| `SECRET_KEY` | JWT signing secret (auto-generated by Render) |
| `ADMIN_NAME` | Admin user display name |
| `ADMIN_PIN` | Admin initial PIN (must be changed on first login) |

---

## Local Setup

```bash
git clone https://github.com/kalkulisto/poker-bankroll-tracker.git
cd poker-bankroll-tracker/backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Place your Google service account JSON as `freckenhorst2-4eb32a77e61f.json` in the backend folder, or set `GOOGLE_CREDENTIALS` as an environment variable.

The frontend is served automatically by FastAPI from `../frontend/`.

---

## Deployment (Render)

- **Root directory:** `backend/`
- **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Instance type:** Free (spins down after 15 min inactivity, ~30s cold start)
- **Auto-deploy:** on every push to `main`

> On startup, `init_sheets()` runs `_ensure_columns()` for all sheets — missing columns are added automatically, making schema migrations safe.

---

## Project Structure

```
poker-bankroll-tracker/
├── backend/
│   ├── main.py                  # FastAPI app, startup, PWA file routes
│   ├── auth.py                  # PIN hashing, JWT creation/verification
│   ├── sheets.py                # Google Sheets CRUD (insert/update/delete/query)
│   └── routers/
│       ├── auth_router.py       # Login, user management, PIN change
│       ├── sessions_router.py   # Cash game CRUD
│       ├── tournaments_router.py # Tournament + entry CRUD, cascade delete
│       └── stats_router.py      # All statistics, leaderboard, badges, challenge
└── frontend/
    ├── index.html               # Single-file Vanilla JS PWA (all UI + logic)
    ├── manifest.json            # PWA manifest (name, icons, display mode)
    ├── sw.js                    # Service Worker (network-first, API bypass)
    ├── icon-192.png             # PWA icon
    └── icon-512.png             # PWA icon (large)
```

---

## Planned Features

- **Tournament tags** (e.g. "Challenge" / "Las Vegas 2026") for separate filtered leaderboards — planned for September 2026 before Vegas trip
- **PIN change UI** for logged-in users

---

*Built for two poker players heading to Las Vegas 🎰 — October 2026*
