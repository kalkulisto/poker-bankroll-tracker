import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import init_db, SessionLocal, User
from auth import hash_pin
from routers.auth_router import router as auth_router
from routers.sessions_router import router as sessions_router
from routers.tournaments_router import router as tournaments_router
from routers.stats_router import router as stats_router

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
    init_db()
    _create_default_admin()


def _create_default_admin():
    admin_name = os.getenv("ADMIN_NAME", "Andreas")
    admin_pin = os.getenv("ADMIN_PIN", "1234")

    db = SessionLocal()
    try:
        if not db.query(User).filter(User.name == admin_name).first():
            admin = User(name=admin_name, pin_hash=hash_pin(admin_pin), is_admin=True)
            db.add(admin)
            db.commit()
            print(f"✅ Admin-User '{admin_name}' angelegt (PIN: {admin_pin})")
    finally:
        db.close()


frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    def serve_frontend():
        return FileResponse(os.path.join(frontend_path, "index.html"))


@app.get("/health")
def health():
    return {"status": "ok"}
