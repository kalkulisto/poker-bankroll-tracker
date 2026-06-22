from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
import sheets
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


def to_dict(r: dict) -> dict:
    buy_in = float(r["buy_in"]) if r["buy_in"] else 0
    cash_out = float(r["cash_out"]) if r["cash_out"] else 0
    return {
        "id": int(r["id"]),
        "date": r["date"],
        "location": r["location"] or None,
        "game_type": r["game_type"],
        "stakes": r["stakes"] or None,
        "buy_in": buy_in,
        "cash_out": cash_out,
        "profit": round(cash_out - buy_in, 2),
        "duration_minutes": int(r["duration_minutes"]) if r["duration_minutes"] else None,
        "notes": r["notes"] or None,
    }


@router.get("/")
def get_sessions(current_user: dict = Depends(get_current_user)):
    rows = sheets.all_rows("poker_sessions")
    uid = int(current_user["id"])
    data = [to_dict(r) for r in rows if int(r["user_id"]) == uid]
    return sorted(data, key=lambda x: x["date"], reverse=True)


@router.post("/")
def create_session(req: SessionCreate, current_user: dict = Depends(get_current_user)):
    sid = sheets.next_id("poker_sessions")
    data = {
        "id": sid, "user_id": int(current_user["id"]),
        "date": str(req.date), "location": req.location or "",
        "game_type": req.game_type, "stakes": req.stakes or "",
        "buy_in": req.buy_in, "cash_out": req.cash_out,
        "duration_minutes": req.duration_minutes or "",
        "notes": req.notes or "", "created_at": datetime.utcnow().isoformat()
    }
    sheets.insert_row("poker_sessions", data)
    data["profit"] = round(req.cash_out - req.buy_in, 2)
    return data


@router.put("/{session_id}")
def update_session(session_id: int, req: SessionCreate, current_user: dict = Depends(get_current_user)):
    row = sheets.get_row("poker_sessions", session_id)
    if not row or int(row["user_id"]) != int(current_user["id"]):
        raise HTTPException(status_code=404, detail="Session nicht gefunden")
    data = {
        "date": str(req.date), "location": req.location or "",
        "game_type": req.game_type, "stakes": req.stakes or "",
        "buy_in": req.buy_in, "cash_out": req.cash_out,
        "duration_minutes": req.duration_minutes or "",
        "notes": req.notes or ""
    }
    sheets.update_row("poker_sessions", session_id, data)
    return {**data, "id": session_id, "profit": round(req.cash_out - req.buy_in, 2)}


@router.delete("/{session_id}")
def delete_session(session_id: int, current_user: dict = Depends(get_current_user)):
    row = sheets.get_row("poker_sessions", session_id)
    if not row or int(row["user_id"]) != int(current_user["id"]):
        raise HTTPException(status_code=404, detail="Session nicht gefunden")
    sheets.delete_row("poker_sessions", session_id)
    return {"ok": True}
