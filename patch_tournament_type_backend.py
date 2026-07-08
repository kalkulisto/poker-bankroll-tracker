import os, json

# Backend: tournament_type zum Schema hinzufuegen
sheets_path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/backend/sheets.py'
with open(sheets_path, encoding='utf-8') as f:
    c = f.read()

old = '"poker_tournaments": ["id", "name", "series", "location", "start_date", "end_date", "buy_in", "game_type", "is_global", "created_by", "field_size", "created_at"],'
new = '"poker_tournaments": ["id", "name", "series", "location", "start_date", "end_date", "buy_in", "game_type", "is_global", "created_by", "field_size", "tournament_type", "created_at"],'

if old in c:
    c = c.replace(old, new, 1)
    print('sheets.py patched')
else:
    print('sheets.py NOT FOUND')

with open(sheets_path, 'w', encoding='utf-8') as f:
    f.write(c)

# tournaments_router: tournament_type in TournamentCreate + t_dict + CRUD
router_path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/backend/routers/tournaments_router.py'
with open(router_path, encoding='utf-8') as f:
    r = f.read()

# TournamentCreate Model
old_model = '    field_size: Optional[int] = None'
new_model = '    field_size: Optional[int] = None\n    tournament_type: Optional[str] = "Live"  # Live / Online'
r = r.replace(old_model, new_model, 1)

# t_dict
old_tdict = '        "field_size": int(t["field_size"]) if t.get("field_size") else None,'
new_tdict = '        "field_size": int(t["field_size"]) if t.get("field_size") else None,\n        "tournament_type": t.get("tournament_type") or "Live",'
r = r.replace(old_tdict, new_tdict, 1)

# create_tournament
old_create = '        "field_size": req.field_size or "",\n        "created_at": datetime.utcnow().isoformat()'
new_create = '        "field_size": req.field_size or "",\n        "tournament_type": req.tournament_type or "Live",\n        "created_at": datetime.utcnow().isoformat()'
r = r.replace(old_create, new_create, 1)

# update_tournament
old_update = '        "field_size": req.field_size or "",\n    }'
new_update = '        "field_size": req.field_size or "",\n        "tournament_type": req.tournament_type or "Live",\n    }'
r = r.replace(old_update, new_update, 1)

with open(router_path, 'w', encoding='utf-8') as f:
    f.write(r)
print('tournaments_router.py patched')
