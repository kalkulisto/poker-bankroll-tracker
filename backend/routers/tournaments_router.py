from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session as DBSession
from typing import Optional
from datetime import date
from database import get_db, Tournament, TournamentEntry, User
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


def tournament_to_dict(t: Tournament, user_entry: Optional[TournamentEntry] = None) -> dict:
    return {
        "id": t.id,
        "name": t.name,
        "series": t.series,
        "location": t.location,
        "start_date": t.start_date.isoformat() if t.start_date else None,
        "end_date": t.end_date.isoformat() if t.end_date else None,
        "buy_in": t.buy_in,
        "game_type": t.game_type,
        "is_global": t.is_global,
        "created_by_name": t.creator.name if t.creator else "System",
        "entry": {
            "id": user_entry.id,
            "result_position": user_entry.result_position,
            "prize_money": user_entry.prize_money,
            "notes": user_entry.notes,
        } if user_entry else None,
    }


@router.get("/")
def get_tournaments(db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    tournaments = db.query(Tournament).filter(
        (Tournament.is_global == True) | (Tournament.created_by == current_user.id)
    ).order_by(Tournament.start_date.asc()).all()

    result = []
    for t in tournaments:
        entry = db.query(TournamentEntry).filter(
            TournamentEntry.tournament_id == t.id,
            TournamentEntry.user_id == current_user.id
        ).first()
        result.append(tournament_to_dict(t, entry))
    return result


@router.post("/")
def create_tournament(
    req: TournamentCreate,
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if req.is_global and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Nur Admins können globale Turniere anlegen")
    t = Tournament(created_by=current_user.id, **req.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return tournament_to_dict(t)


@router.put("/{tournament_id}")
def update_tournament(
    tournament_id: int,
    req: TournamentCreate,
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    t = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Nicht gefunden")
    if t.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Keine Berechtigung")
    if req.is_global and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Nur Admins können Turniere global setzen")
    for k, v in req.model_dump().items():
        setattr(t, k, v)
    db.commit()
    return tournament_to_dict(t)


@router.delete("/{tournament_id}")
def delete_tournament(
    tournament_id: int,
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    t = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Nicht gefunden")
    if t.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Keine Berechtigung")
    db.delete(t)
    db.commit()
    return {"ok": True}


@router.put("/{tournament_id}/entry")
def upsert_entry(
    tournament_id: int,
    req: EntryUpsert,
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    t = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Turnier nicht gefunden")

    entry = db.query(TournamentEntry).filter(
        TournamentEntry.tournament_id == tournament_id,
        TournamentEntry.user_id == current_user.id
    ).first()

    if entry:
        entry.result_position = req.result_position
        entry.prize_money = req.prize_money
        entry.notes = req.notes
    else:
        entry = TournamentEntry(
            user_id=current_user.id,
            tournament_id=tournament_id,
            **req.model_dump()
        )
        db.add(entry)

    db.commit()
    db.refresh(entry)
    return {"id": entry.id, "result_position": entry.result_position, "prize_money": entry.prize_money}


@router.delete("/{tournament_id}/entry")
def delete_entry(
    tournament_id: int,
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entry = db.query(TournamentEntry).filter(
        TournamentEntry.tournament_id == tournament_id,
        TournamentEntry.user_id == current_user.id
    ).first()
    if entry:
        db.delete(entry)
        db.commit()
    return {"ok": True}
