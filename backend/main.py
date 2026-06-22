import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sheets import init_sheets, all_rows, next_id, insert_row, update_row
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

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")


@app.on_event("startup")
def startup():
    print("Initialisiere Sheets...")
    init_sheets()
    _create_default_admin()
    print("Fertig")


def _create_default_admin():
    admin_name = os.getenv("ADMIN_NAME", "Andreas")
    admin_pin = os.getenv("ADMIN_PIN", "1234")
    users = all_rows("poker_users")
    existing = next((u for u in users if u["name"] == admin_name), None)
    if not existing:
        uid = next_id("poker_users")
        insert_row("poker_users", {
            "id": uid, "name": admin_name, "pin_hash": hash_pin(admin_pin),
            "is_admin": "True", "pin_changed": "True",
            "created_at": datetime.utcnow().isoformat()
        })
        print(f"Admin '{admin_name}' angelegt")
    else:
        if str(existing.get("pin_changed", "")).lower() != "true":
            update_row("poker_users", int(existing["id"]), {"pin_changed": "True"})


# PWA-Dateien direkt an der Wurzel servieren (wichtig fuer Service Worker Scope)
@app.get("/sw.js")
def serve_sw():
    return FileResponse(os.path.join(frontend_path, "sw.js"), media_type="application/javascript")

@app.get("/manifest.json")
def serve_manifest():
    return FileResponse(os.path.join(frontend_path, "manifest.json"), media_type="application/manifest+json")

@app.get("/icon-192.png")
def serve_icon_192():
    return FileResponse(os.path.join(frontend_path, "icon-192.png"), media_type="image/png")

@app.get("/icon-512.png")
def serve_icon_512():
    return FileResponse(os.path.join(frontend_path, "icon-512.png"), media_type="image/png")


# Statische Dateien
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    def serve_frontend():
        return FileResponse(os.path.join(frontend_path, "index.html"))


@app.get("/health")
def health():
    return {"status": "ok"}
