from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
import sheets
from auth import get_current_user

router = APIRouter(prefix="/tournaments", tags=["tournaments"])


class TournamentCreate(BaseModel):
    name: str
    series: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    buy_in: Optional[float] = None
    game_type: str = "NL Hold'em"
    is_global: bool = False


class EntryUpsert(BaseModel):
    result_position: Optional[int] = None
    prize_money: float = 0.0
    notes: Optional[str] = None


def t_dict(t: dict, entry: dict | None = None) -> dict:
    users = sheets.all_rows("poker_users")
    creator = next((u for u in users if str(u["id"]) == str(t["created_by"])), None)
    return {
        "id": int(t["id"]),
        "name": t["name"],
        "series": t["series"] or None,
        "location": t["location"] or None,
        "start_date": t["start_date"] or None,
        "end_date": t["end_date"] or None,
        "buy_in": float(t["buy_in"]) if t["buy_in"] else None,
        "game_type": t["game_type"],
        "is_global": str(t["is_global"]).lower() == "true",
        "created_by_name": creator["name"] if creator else "System",
        "entry": {
            "id": int(entry["id"]),
            "result_position": int(entry["result_position"]) if entry["result_position"] else None,
            "prize_money": float(entry["prize_money"]) if entry["prize_money"] else 0.0,
            "notes": entry["notes"] or None,
        } if entry else None,
    }


@router.get("/")
def get_tournaments(current_user: dict = Depends(get_current_user)):
    uid = int(current_user["id"])
    tournaments = sheets.all_rows("poker_tournaments")
    entries = sheets.all_rows("poker_entries")

    result = []
    for t in tournaments:
        is_global = str(t["is_global"]).lower() == "true"
        created_by = int(t["created_by"]) if t["created_by"] else None
        if not is_global and created_by != uid:
            continue
        entry = next((e for e in entries if int(e["tournament_id"]) == int(t["id"]) and int(e["user_id"]) == uid), None)
        result.append(t_dict(t, entry))

    return sorted(result, key=lambda x: x["start_date"] or "9999", reverse=False)


@router.post("/")
def create_tournament(req: TournamentCreate, current_user: dict = Depends(get_current_user)):
    if req.is_global and str(current_user.get("is_admin", "")).lower() != "true":
        raise HTTPException(status_code=403, detail="Nur Admins können globale Turniere anlegen")
    tid = sheets.next_id("poker_tournaments")
    data = {
        "id": tid, "name": req.name, "series": req.series or "",
        "location": req.location or "", "start_date": str(req.start_date) if req.start_date else "",
        "end_date": str(req.end_date) if req.end_date else "",
        "buy_in": req.buy_in or "", "game_type": req.game_type,
        "is_global": str(req.is_global), "created_by": int(current_user["id"]),
        "created_at": datetime.utcnow().isoformat()
    }
    sheets.insert_row("poker_tournaments", data)
    return t_dict(data)


@router.put("/{tournament_id}")
def update_tournament(tournament_id: int, req: TournamentCreate, current_user: dict = Depends(get_current_user)):
    t = sheets.get_row("poker_tournaments", tournament_id)
    if not t:
        raise HTTPException(status_code=404, detail="Nicht gefunden")
    if int(t["created_by"]) != int(current_user["id"]) and str(current_user.get("is_admin", "")).lower() != "true":
        raise HTTPException(status_code=403, detail="Keine Berechtigung")
    if req.is_global and str(current_user.get("is_admin", "")).lower() != "true":
        raise HTTPException(status_code=403, detail="Nur Admins können global setzen")
    data = {
        "name": req.name, "series": req.series or "", "location": req.location or "",
        "start_date": str(req.start_date) if req.start_date else "",
        "end_date": str(req.end_date) if req.end_date else "",
        "buy_in": req.buy_in or "", "game_type": req.game_type, "is_global": str(req.is_global)
    }
    sheets.update_row("poker_tournaments", tournament_id, data)
    return t_dict({**t, **data})


@router.delete("/{tournament_id}")
def delete_tournament(tournament_id: int, current_user: dict = Depends(get_current_user)):
    t = sheets.get_row("poker_tournaments", tournament_id)
    if not t:
        raise HTTPException(status_code=404, detail="Nicht gefunden")
    if int(t["created_by"]) != int(current_user["id"]) and str(current_user.get("is_admin", "")).lower() != "true":
        raise HTTPException(status_code=403, detail="Keine Berechtigung")
    sheets.delete_row("poker_tournaments", tournament_id)
    return {"ok": True}


@router.put("/{tournament_id}/entry")
def upsert_entry(tournament_id: int, req: EntryUpsert, current_user: dict = Depends(get_current_user)):
    t = sheets.get_row("poker_tournaments", tournament_id)
    if not t:
        raise HTTPException(status_code=404, detail="Turnier nicht gefunden")
    uid = int(current_user["id"])
    entries = sheets.all_rows("poker_entries")
    existing = next((e for e in entries if int(e["tournament_id"]) == tournament_id and int(e["user_id"]) == uid), None)

    if existing:
        sheets.update_row("poker_entries", int(existing["id"]), {
            "result_position": req.result_position or "",
            "prize_money": req.prize_money, "notes": req.notes or ""
        })
        return {"id": int(existing["id"]), "result_position": req.result_position, "prize_money": req.prize_money}
    else:
        eid = sheets.next_id("poker_entries")
        data = {
            "id": eid, "user_id": uid, "tournament_id": tournament_id,
            "result_position": req.result_position or "", "prize_money": req.prize_money,
            "notes": req.notes or "", "created_at": datetime.utcnow().isoformat()
        }
        sheets.insert_row("poker_entries", data)
        return {"id": eid, "result_position": req.result_position, "prize_money": req.prize_money}


@router.delete("/{tournament_id}/entry")
def delete_entry(tournament_id: int, current_user: dict = Depends(get_current_user)):
    uid = int(current_user["id"])
    entries = sheets.all_rows("poker_entries")
    existing = next((e for e in entries if int(e["tournament_id"]) == tournament_id and int(e["user_id"]) == uid), None)
    if existing:
        sheets.delete_row("poker_entries", int(existing["id"]))
    return {"ok": True}
