from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession
from database import get_db, Session, TournamentEntry, User
from auth import get_current_user
from collections import defaultdict

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/summary")
def get_summary(db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    sessions = db.query(Session).filter(Session.user_id == current_user.id).all()

    if not sessions:
        return {
            "total_sessions": 0, "total_profit": 0, "total_buy_in": 0,
            "win_rate": 0, "roi": 0, "avg_profit_per_session": 0,
            "total_hours": 0, "profit_per_hour": 0,
            "biggest_win": 0, "biggest_loss": 0, "current_streak": 0,
        }

    profits = [s.cash_out - s.buy_in for s in sessions]
    total_buy_in = sum(s.buy_in for s in sessions)
    total_profit = sum(profits)
    wins = [p for p in profits if p > 0]
    total_minutes = sum(s.duration_minutes or 0 for s in sessions)
    total_hours = total_minutes / 60

    sorted_profits = [s.cash_out - s.buy_in for s in sorted(sessions, key=lambda x: x.date, reverse=True)]
    streak = 0
    if sorted_profits:
        sign = 1 if sorted_profits[0] >= 0 else -1
        for p in sorted_profits:
            if (p >= 0 and sign == 1) or (p < 0 and sign == -1):
                streak += sign
            else:
                break

    return {
        "total_sessions": len(sessions),
        "total_profit": round(total_profit, 2),
        "total_buy_in": round(total_buy_in, 2),
        "win_rate": round(len(wins) / len(sessions) * 100, 1),
        "roi": round(total_profit / total_buy_in * 100, 1) if total_buy_in > 0 else 0,
        "avg_profit_per_session": round(total_profit / len(sessions), 2),
        "total_hours": round(total_hours, 1),
        "profit_per_hour": round(total_profit / total_hours, 2) if total_hours > 0 else 0,
        "biggest_win": round(max(profits), 2),
        "biggest_loss": round(min(profits), 2),
        "current_streak": streak,
    }


@router.get("/monthly")
def get_monthly(db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    sessions = db.query(Session).filter(Session.user_id == current_user.id).all()
    monthly = defaultdict(lambda: {"profit": 0, "sessions": 0, "buy_in": 0})
    for s in sessions:
        key = f"{s.date.year}-{s.date.month:02d}"
        monthly[key]["profit"] += round(s.cash_out - s.buy_in, 2)
        monthly[key]["sessions"] += 1
        monthly[key]["buy_in"] += s.buy_in
    return [{"month": k, **v} for k, v in sorted(monthly.items())]


@router.get("/tournaments")
def get_tournament_stats(db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    entries = db.query(TournamentEntry).filter(TournamentEntry.user_id == current_user.id).all()
    if not entries:
        return {"total_entered": 0, "total_invested": 0, "total_winnings": 0, "tournament_profit": 0, "itm_rate": 0}

    total_invested = sum(e.tournament.buy_in or 0 for e in entries if e.tournament)
    total_winnings = sum(e.prize_money or 0 for e in entries)
    itm = len([e for e in entries if (e.prize_money or 0) > 0])

    return {
        "total_entered": len(entries),
        "total_invested": round(total_invested, 2),
        "total_winnings": round(total_winnings, 2),
        "tournament_profit": round(total_winnings - total_invested, 2),
        "itm_rate": round(itm / len(entries) * 100, 1),
    }
