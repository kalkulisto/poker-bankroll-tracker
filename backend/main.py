import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sheets import init_sheets, all_rows, next_id, insert_row
from auth import hash_pin
from routers.auth_router import router as auth_router
from routers.sessions_router import router as sessions_router
from routers.tournaments_router import router as tournaments_router
from routers.stats_router import router as stats_router
from datetime import datetime

app = FastAPI(title="Poker Bankroll Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(sessions_router)
app.include_router(tournaments_router)
app.include_router(stats_router)


@app.on_event("startup")
def startup():
    print("🃏 Initialisiere Sheets...")
    init_sheets()
    _create_default_admin()
    print("✅ Fertig")


def _create_default_admin():
    admin_name = os.getenv("ADMIN_NAME", "Andreas")
    admin_pin = os.getenv("ADMIN_PIN", "1234")
    users = all_rows("poker_users")
    if not any(u["name"] == admin_name for u in users):
        uid = next_id("poker_users")
        insert_row("poker_users", {
            "id": uid, "name": admin_name, "pin_hash": hash_pin(admin_pin),
            "is_admin": "True", "created_at": datetime.utcnow().isoformat()
        })
        print(f"✅ Admin '{admin_name}' angelegt")


frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    def serve_frontend():
        return FileResponse(os.path.join(frontend_path, "index.html"))


@app.get("/health")
def health():
    return {"status": "ok"}
