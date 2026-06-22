import os
import json
import gspread
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = "1TwTc5_24NcM2qV5JRNY5RQjO8ClckGGzNivG5RNFQ4Y"

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

SHEET_SCHEMAS = {
    "poker_users":       ["id", "name", "pin_hash", "is_admin", "created_at"],
    "poker_sessions":    ["id", "user_id", "date", "location", "game_type", "stakes", "buy_in", "cash_out", "duration_minutes", "notes", "created_at"],
    "poker_tournaments": ["id", "name", "series", "location", "start_date", "end_date", "buy_in", "game_type", "is_global", "created_by", "created_at"],
    "poker_entries":     ["id", "user_id", "tournament_id", "result_position", "prize_money", "notes", "created_at"],
}


def get_client():
    creds_json = os.environ.get("GOOGLE_CREDENTIALS")
    if creds_json:
        creds = Credentials.from_service_account_info(json.loads(creds_json), scopes=SCOPES)
    else:
        creds = Credentials.from_service_account_file("freckenhorst2-4eb32a77e61f.json", scopes=SCOPES)
    return gspread.authorize(creds)


def get_spreadsheet():
    return get_client().open_by_key(SPREADSHEET_ID)


def get_sheet(name: str):
    """Holt ein Sheet, legt es an falls nicht vorhanden."""
    ss = get_spreadsheet()
    try:
        ws = ss.worksheet(name)
    except gspread.WorksheetNotFound:
        ws = ss.add_worksheet(title=name, rows=1000, cols=len(SHEET_SCHEMAS[name]))
        ws.append_row(SHEET_SCHEMAS[name])
    return ws


def init_sheets():
    """Legt alle benötigten Sheets beim Start an."""
    for name in SHEET_SCHEMAS:
        get_sheet(name)


# ── CRUD Hilfsfunktionen ───────────────────────────────────────────────────────

def all_rows(sheet_name: str) -> list[dict]:
    ws = get_sheet(sheet_name)
    records = ws.get_all_records()
    return records


def get_row(sheet_name: str, row_id: int) -> dict | None:
    rows = all_rows(sheet_name)
    for r in rows:
        if int(r["id"]) == row_id:
            return r
    return None


def next_id(sheet_name: str) -> int:
    rows = all_rows(sheet_name)
    if not rows:
        return 1
    return max(int(r["id"]) for r in rows) + 1


def insert_row(sheet_name: str, data: dict) -> dict:
    ws = get_sheet(sheet_name)
    headers = SHEET_SCHEMAS[sheet_name]
    row = [str(data.get(h, "")) for h in headers]
    ws.append_row(row)
    return data


def update_row(sheet_name: str, row_id: int, data: dict):
    ws = get_sheet(sheet_name)
    records = ws.get_all_records()
    headers = SHEET_SCHEMAS[sheet_name]
    for i, r in enumerate(records):
        if int(r["id"]) == row_id:
            sheet_row = i + 2  # +1 header, +1 1-indexed
            for col_idx, header in enumerate(headers, start=1):
                if header in data:
                    ws.update_cell(sheet_row, col_idx, str(data[header]))
            return True
    return False


def delete_row(sheet_name: str, row_id: int):
    ws = get_sheet(sheet_name)
    records = ws.get_all_records()
    for i, r in enumerate(records):
        if int(r["id"]) == row_id:
            ws.delete_rows(i + 2)
            return True
    return False
