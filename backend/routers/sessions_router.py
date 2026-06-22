from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session as DBSession
from typing import Optional
from datetime import date
from database import get_db, Session, User
from auth import get_current_user

router = APIRouter(prefix="/sessions", tags=["sessions"])


class SessionCreate(BaseModel):
    date: date
    location: Optional[str] = None
    game_type: str = "NL Hold'em"
    stakes: Optional[str] = None
    buy_in: float
    cash_out: float
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None


def session_to_dict(s: Session) -> dict:
    return {
        "id": s.id,
        "date": s.date.isoformat(),
        "location": s.location,
        "game_type": s.game_type,
        "stakes": s.stakes,
        "buy_in": s.buy_in,
        "cash_out": s.cash_out,
        "profit": round(s.cash_out - s.buy_in, 2),
        "duration_minutes": s.duration_minutes,
        "notes": s.notes,
    }


@router.get("/")
def get_sessions(db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    sessions = db.query(Session).filter(Session.user_id == current_user.id).order_by(Session.date.desc()).all()
    return [session_to_dict(s) for s in sessions]


@router.post("/")
def create_session(req: SessionCreate, db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    s = Session(user_id=current_user.id, **req.model_dump())
    db.add(s)
    db.commit()
    db.refresh(s)
    return session_to_dict(s)


@router.put("/{session_id}")
def update_session(session_id: int, req: SessionCreate, db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    s = db.query(Session).filter(Session.id == session_id, Session.user_id == current_user.id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Session nicht gefunden")
    for k, v in req.model_dump().items():
        setattr(s, k, v)
    db.commit()
    return session_to_dict(s)


@router.delete("/{session_id}")
def delete_session(session_id: int, db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    s = db.query(Session).filter(Session.id == session_id, Session.user_id == current_user.id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Session nicht gefunden")
    db.delete(s)
    db.commit()
    return {"ok": True}
