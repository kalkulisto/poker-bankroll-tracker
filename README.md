# 🃏 Chico und Zwieback — Poker Bankroll Tracker

A personal poker bankroll tracker PWA built for two players, featuring cash game tracking, tournament management, head-to-head leaderboard, and a 100-tournament challenge.

**Live:** https://poker-bankroll-tracker-7mk8.onrender.com

---

## Features

- **PIN-based login** for two players (SHA256 + JWT)
- **Cash Games** — track sessions with buy-in, cash-out, duration, stakes
- **Tournaments** — calendar with global (shared) and personal entries
- **Reentries** — effective buy-in calculated as `buy_in × (reentries + 1)`
- **Head-to-Head Leaderboard** with badges (ITM, Final Table, Top 3, Top 10%, Biggest Win)
- **100-Tournament Challenge** with progress bar, live gap indicator, form dots (last 8 results), milestone popups with confetti at 25/50/75/100
- **Stats** — Cash-Stats, Turnier-Stats, combined Gesamt view with cumulative timeline chart
- **PWA** — installable on Android and iOS, works offline (cached shell)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Database | Google Sheets (via gspread) |
| Frontend | Vanilla JS, single-file HTML PWA |
| Hosting | Render (Free tier) |
| Auth | SHA256 PIN hash + JWT |

---

## Google Sheets Schema

All data lives in a single Google Spreadsheet. Four sheets are required:

### `poker_users`
| Column | Type | Description |
|---|---|---|
| id | int | Auto-increment |
| name | string | Display name |
| pin_hash | string | SHA256 hash of PIN |
| is_admin | bool | Admin flag |
| pin_changed | bool | First-login PIN change flag |
| created_at | datetime | ISO timestamp |

### `poker_sessions` (Cash Games)
| Column | Type | Description |
|---|---|---|
| id | int | Auto-increment |
| user_id | int | FK → poker_users |
| date | date | YYYY-MM-DD |
| location | string | Casino / location |
| game_type | string | NL Hold'em / PLO |
| stakes | string | e.g. 1/2, 2/5 |
| buy_in | float | Buy-in amount ($) |
| cash_out | float | Cash-out amount ($) |
| duration_minutes | int | Session duration |
| notes | string | Optional notes |
| created_at | datetime | ISO timestamp |

### `poker_tournaments`
| Column | Type | Description |
|---|---|---|
| id | int | Auto-increment |
| name | string | Tournament name |
| series | string | e.g. WSOP, Wynn |
| location | string | Casino / platform |
| start_date | date | YYYY-MM-DD |
| end_date | date | YYYY-MM-DD |
| buy_in | float | Buy-in amount ($) |
| game_type | string | NL Hold'em / PLO |
| is_global | bool | Visible to all users |
| created_by | int | FK → poker_users |
| field_size | int | Number of entrants (optional, for Top 10% badge) |
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

---

## Environment Variables (Render)

| Variable | Description |
|---|---|
| `GOOGLE_CREDENTIALS` | Service account JSON (stringified) |
| `SECRET_KEY` | JWT signing secret |
| `ADMIN_NAME` | Admin user display name |
| `ADMIN_PIN` | Admin initial PIN |

---

## Local Setup

```bash
git clone https://github.com/kalkulisto/poker-bankroll-tracker.git
cd poker-bankroll-tracker/backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Place your Google service account JSON as `freckenhorst2-4eb32a77e61f.json` in the backend folder, or set `GOOGLE_CREDENTIALS` as environment variable.

---

## Deployment

Hosted on Render as a Web Service:
- **Root directory:** `backend/`
- **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Auto-deploy:** on push to `main`

---

## Project Structure

```
poker-bankroll-tracker/
├── backend/
│   ├── main.py              # FastAPI app, startup, static file serving
│   ├── auth.py              # PIN hashing, JWT, dependencies
│   ├── sheets.py            # Google Sheets CRUD layer
│   └── routers/
│       ├── auth_router.py
│       ├── sessions_router.py
│       ├── tournaments_router.py
│       └── stats_router.py
└── frontend/
    ├── index.html           # Single-file Vanilla JS PWA
    ├── manifest.json        # PWA manifest
    ├── sw.js                # Service Worker
    ├── icon-192.png
    └── icon-512.png
```

---

*Built for two poker players heading to Las Vegas 🎰*
