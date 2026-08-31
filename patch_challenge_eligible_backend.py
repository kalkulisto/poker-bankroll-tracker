import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. sheets.py: challenge_eligible zum Schema hinzufuegen
sheets_path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/backend/sheets.py'
with open(sheets_path, encoding='utf-8') as f:
    c = f.read()

old = '"poker_tournaments": ["id", "name", "series", "location", "start_date", "end_date", "buy_in", "game_type", "is_global", "created_by", "field_size", "tournament_type", "created_at"],'
new = '"poker_tournaments": ["id", "name", "series", "location", "start_date", "end_date", "buy_in", "game_type", "is_global", "created_by", "field_size", "tournament_type", "challenge_eligible", "created_at"],'

if old in c:
    c = c.replace(old, new, 1)
    print('sheets.py patched')
else:
    print('sheets.py NOT FOUND')

with open(sheets_path, 'w', encoding='utf-8') as f:
    f.write(c)

# 2. tournaments_router.py: challenge_eligible in Model, t_dict, create, update
router_path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/backend/routers/tournaments_router.py'
with open(router_path, encoding='utf-8') as f:
    r = f.read()

r = r.replace(
    '    tournament_type: Optional[str] = "Live"  # Live / Online',
    '    tournament_type: Optional[str] = "Live"  # Live / Online\n    challenge_eligible: bool = True'
)
r = r.replace(
    '        "tournament_type": t.get("tournament_type") or "Live",',
    '        "tournament_type": t.get("tournament_type") or "Live",\n        "challenge_eligible": str(t.get("challenge_eligible", "True")).lower() != "false",'
)
r = r.replace(
    '        "tournament_type": req.tournament_type or "Live",\n        "created_at": datetime.utcnow().isoformat()',
    '        "tournament_type": req.tournament_type or "Live",\n        "challenge_eligible": str(req.challenge_eligible),\n        "created_at": datetime.utcnow().isoformat()'
)
r = r.replace(
    '        "field_size": req.field_size or "",\n        "tournament_type": req.tournament_type or "Live",\n    }',
    '        "field_size": req.field_size or "",\n        "tournament_type": req.tournament_type or "Live",\n        "challenge_eligible": str(req.challenge_eligible),\n    }'
)

with open(router_path, 'w', encoding='utf-8') as f:
    f.write(r)
print('tournaments_router.py patched')
