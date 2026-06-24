from fastapi import APIRouter, Depends
from collections import defaultdict
import sheets
from auth import get_current_user

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/summary")
def get_summary(current_user: dict = Depends(get_current_user)):
    uid = int(current_user["id"])
    rows = sheets.all_rows("poker_sessions")
    sessions = [r for r in rows if int(r["user_id"]) == uid]

    if not sessions:
        return {"total_sessions": 0, "total_profit": 0, "total_buy_in": 0,
                "win_rate": 0, "roi": 0, "avg_profit_per_session": 0,
                "total_hours": 0, "profit_per_hour": 0, "biggest_win": 0,
                "biggest_loss": 0, "current_streak": 0}

    profits = [float(s["cash_out"]) - float(s["buy_in"]) for s in sessions]
    total_buy_in = sum(float(s["buy_in"]) for s in sessions)
    total_profit = sum(profits)
    wins = [p for p in profits if p > 0]
    total_minutes = sum(int(s["duration_minutes"]) for s in sessions if s["duration_minutes"])
    total_hours = total_minutes / 60

    sorted_profits = [float(s["cash_out"]) - float(s["buy_in"])
                      for s in sorted(sessions, key=lambda x: x["date"], reverse=True)]
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
def get_monthly(current_user: dict = Depends(get_current_user)):
    uid = int(current_user["id"])
    rows = sheets.all_rows("poker_sessions")
    sessions = [r for r in rows if int(r["user_id"]) == uid]
    monthly = defaultdict(lambda: {"profit": 0, "sessions": 0, "buy_in": 0})
    for s in sessions:
        key = s["date"][:7]
        p = float(s["cash_out"]) - float(s["buy_in"])
        monthly[key]["profit"] += round(p, 2)
        monthly[key]["sessions"] += 1
        monthly[key]["buy_in"] += float(s["buy_in"])
    return [{"month": k, **v} for k, v in sorted(monthly.items())]


@router.get("/tournaments")
def get_tournament_stats(current_user: dict = Depends(get_current_user)):
    uid = int(current_user["id"])
    all_entries = sheets.all_rows("poker_entries")
    tournaments = {int(t["id"]): t for t in sheets.all_rows("poker_tournaments")}

    entries = [e for e in all_entries
               if int(e["user_id"]) == uid and int(e["tournament_id"]) in tournaments]

    if not entries:
        return {"total_entered": 0, "total_invested": 0, "total_winnings": 0,
                "tournament_profit": 0, "itm_rate": 0, "monthly": []}

    total_invested = sum(float(tournaments[int(e["tournament_id"])]["buy_in"] or 0) for e in entries)
    total_winnings = sum(float(e["prize_money"] or 0) for e in entries)
    itm = len([e for e in entries if float(e["prize_money"] or 0) > 0])

    monthly = defaultdict(lambda: {"profit": 0, "tournaments": 0, "invested": 0})
    for e in entries:
        t = tournaments[int(e["tournament_id"])]
        date = t.get("start_date", "")
        if date:
            key = date[:7]
            buy_in = float(t["buy_in"] or 0)
            prize = float(e["prize_money"] or 0)
            monthly[key]["profit"] += round(prize - buy_in, 2)
            monthly[key]["tournaments"] += 1
            monthly[key]["invested"] += buy_in

    return {
        "total_entered": len(entries),
        "total_invested": round(total_invested, 2),
        "total_winnings": round(total_winnings, 2),
        "tournament_profit": round(total_winnings - total_invested, 2),
        "itm_rate": round(itm / len(entries) * 100, 1),
        "monthly": [{"month": k, **v} for k, v in sorted(monthly.items())],
    }


@router.get("/combined")
def get_combined(current_user: dict = Depends(get_current_user)):
    uid = int(current_user["id"])
    sessions = [r for r in sheets.all_rows("poker_sessions") if int(r["user_id"]) == uid]
    all_entries = sheets.all_rows("poker_entries")
    tournaments = {int(t["id"]): t for t in sheets.all_rows("poker_tournaments")}
    entries = [e for e in all_entries
               if int(e["user_id"]) == uid and int(e["tournament_id"]) in tournaments]

    monthly = defaultdict(lambda: {
        "cash_profit": 0.0, "cash_invested": 0.0, "cash_sessions": 0,
        "tournament_profit": 0.0, "tournament_invested": 0.0, "tournament_count": 0,
    })

    for s in sessions:
        key = s["date"][:7]
        p = float(s["cash_out"]) - float(s["buy_in"])
        monthly[key]["cash_profit"] += round(p, 2)
        monthly[key]["cash_invested"] += float(s["buy_in"])
        monthly[key]["cash_sessions"] += 1

    for e in entries:
        t = tournaments[int(e["tournament_id"])]
        date = t.get("start_date", "")
        if date:
            key = date[:7]
            buy_in = float(t["buy_in"] or 0)
            prize = float(e["prize_money"] or 0)
            monthly[key]["tournament_profit"] += round(prize - buy_in, 2)
            monthly[key]["tournament_invested"] += buy_in
            monthly[key]["tournament_count"] += 1

    return {
        "total_sessions": len(sessions),
        "total_tournaments": len(entries),
        "cash_hours": round(sum(int(s["duration_minutes"]) for s in sessions if s["duration_minutes"]) / 60, 1),
        "monthly": [{"month": k, **v} for k, v in sorted(monthly.items())],
    }


@router.get("/timeline")
def get_timeline(current_user: dict = Depends(get_current_user)):
    """Chronologische Events fuer den kumulativen Zeitverlauf-Chart."""
    uid = int(current_user["id"])
    sessions = [r for r in sheets.all_rows("poker_sessions") if int(r["user_id"]) == uid]
    all_entries = sheets.all_rows("poker_entries")
    tournaments = {int(t["id"]): t for t in sheets.all_rows("poker_tournaments")}
    entries = [e for e in all_entries
               if int(e["user_id"]) == uid and int(e["tournament_id"]) in tournaments]

    events = []

    for s in sessions:
        events.append({
            "date": s["date"],
            "type": "cash",
            "label": s.get("location") or "Cash",
            "profit": round(float(s["cash_out"]) - float(s["buy_in"]), 2),
        })

    for e in entries:
        t = tournaments[int(e["tournament_id"])]
        date = t.get("start_date", "")
        if not date:
            continue
        buy_in = float(t["buy_in"] or 0)
        prize = float(e["prize_money"] or 0)
        events.append({
            "date": date,
            "type": "tournament",
            "label": t["name"],
            "profit": round(prize - buy_in, 2),
        })

    events.sort(key=lambda e: e["date"])
    return events


@router.get("/leaderboard")
def get_leaderboard(current_user: dict = Depends(get_current_user)):
    all_entries = sheets.all_rows("poker_entries")
    all_tournaments = {int(t["id"]): t for t in sheets.all_rows("poker_tournaments")}
    all_users = {int(u["id"]): u["name"] for u in sheets.all_rows("poker_users")}

    valid_entries = [e for e in all_entries if int(e["tournament_id"]) in all_tournaments]

    by_tournament = defaultdict(list)
    for e in valid_entries:
        by_tournament[int(e["tournament_id"])].append(e)

    shared = {tid: entries for tid, entries in by_tournament.items()
              if len(set(int(e["user_id"]) for e in entries)) >= 2}

    user_stats = defaultdict(lambda: {
        "total_profit": 0.0, "total_invested": 0.0, "total_winnings": 0.0,
        "tournaments": 0, "itm": 0, "best_position": None,
    })

    tournaments_detail = []
    for tid, entries in sorted(shared.items(), key=lambda x: all_tournaments.get(x[0], {}).get("start_date", "") or "", reverse=True):
        t = all_tournaments.get(tid)
        if not t:
            continue
        buy_in = float(t["buy_in"] or 0)
        players = []
        for e in entries:
            uid = int(e["user_id"])
            prize = float(e["prize_money"] or 0)
            pos = int(e["result_position"]) if e["result_position"] else None
            profit = prize - buy_in
            players.append({"user_id": uid, "name": all_users.get(uid, "?"),
                             "position": pos, "prize_money": prize, "profit": round(profit, 2)})
            user_stats[uid]["tournaments"] += 1
            user_stats[uid]["total_invested"] += buy_in
            user_stats[uid]["total_winnings"] += prize
            user_stats[uid]["total_profit"] += profit
            if prize > 0:
                user_stats[uid]["itm"] += 1
            if pos and (user_stats[uid]["best_position"] is None or pos < user_stats[uid]["best_position"]):
                user_stats[uid]["best_position"] = pos

        players.sort(key=lambda p: (p["position"] or 9999))
        tournaments_detail.append({
            "id": tid, "name": t["name"], "series": t["series"] or None,
            "start_date": t["start_date"] or None, "buy_in": buy_in, "players": players,
        })

    leaderboard = []
    for uid, stats in user_stats.items():
        itm_rate = round(stats["itm"] / stats["tournaments"] * 100, 1) if stats["tournaments"] else 0
        roi = round(stats["total_profit"] / stats["total_invested"] * 100, 1) if stats["total_invested"] else 0
        leaderboard.append({
            "user_id": uid, "name": all_users.get(uid, "?"),
            "tournaments": stats["tournaments"],
            "total_invested": round(stats["total_invested"], 2),
            "total_winnings": round(stats["total_winnings"], 2),
            "total_profit": round(stats["total_profit"], 2),
            "roi": roi, "itm_rate": itm_rate, "best_position": stats["best_position"],
        })
    leaderboard.sort(key=lambda x: x["total_profit"], reverse=True)

    return {"leaderboard": leaderboard, "tournaments": tournaments_detail}
