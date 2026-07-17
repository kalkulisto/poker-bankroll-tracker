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
    "poker_users":       ["id", "name", "pin_hash", "is_admin", "pin_changed", "created_at"],
    "poker_sessions":    ["id", "user_id", "date", "location", "game_type", "stakes", "buy_in", "cash_out", "duration_minutes", "notes", "created_at"],
    "poker_tournaments": ["id", "name", "series", "location", "start_date", "end_date", "buy_in", "game_type", "is_global", "created_by", "field_size", "tournament_type", "created_at"],
    "poker_entries":     ["id", "user_id", "tournament_id", "result_position", "prize_money", "reentries", "notes", "created_at"],
}

# Caching fuer Client und Spreadsheet
_client = None
_spreadsheet = None
_worksheets = {}


def get_client():
    global _client
    if _client is None:
        creds_json = os.environ.get("GOOGLE_CREDENTIALS")
        if creds_json:
            creds = Credentials.from_service_account_info(json.loads(creds_json), scopes=SCOPES)
        else:
            creds = Credentials.from_service_account_file("freckenhorst2-4eb32a77e61f.json", scopes=SCOPES)
        _client = gspread.authorize(creds)
    return _client


def get_spreadsheet():
    global _spreadsheet
    if _spreadsheet is None:
        _spreadsheet = get_client().open_by_key(SPREADSHEET_ID)
    return _spreadsheet


def get_sheet(name: str):
    global _worksheets
    if name not in _worksheets:
        ss = get_spreadsheet()
        try:
            ws = ss.worksheet(name)
        except gspread.WorksheetNotFound:
            ws = ss.add_worksheet(title=name, rows=1000, cols=len(SHEET_SCHEMAS[name]))
            ws.append_row(SHEET_SCHEMAS[name])
        _worksheets[name] = ws
    return _worksheets[name]


def reset_cache():
    """Cache zuruecksetzen bei Verbindungsfehlern."""
    global _client, _spreadsheet, _worksheets
    _client = None
    _spreadsheet = None
    _worksheets = {}


def _ensure_columns(ws, schema: list[str]):
    actual = ws.row_values(1)
    missing = [col for col in schema if col not in actual]
    if missing:
        for col in missing:
            col_idx = len(actual) + missing.index(col) + 1
            ws.add_cols(1)
            ws.update_cell(1, col_idx, col)


def init_sheets():
    for name, schema in SHEET_SCHEMAS.items():
        ws = get_sheet(name)
        _ensure_columns(ws, schema)


def _safe_call(fn, *args, **kwargs):
    """Wiederholung bei Verbindungsfehlern mit Cache-Reset."""
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        if "RESOURCE_EXHAUSTED" in str(e) or "quota" in str(e).lower() or "connection" in str(e).lower():
            reset_cache()
            return fn(*args, **kwargs)
        raise


def all_rows(sheet_name: str) -> list[dict]:
    ws = get_sheet(sheet_name)
    return _safe_call(ws.get_all_records)


def get_row(sheet_name: str, row_id: int) -> dict | None:
    for r in all_rows(sheet_name):
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
    headers = _safe_call(ws.row_values, 1)
    row = [str(data.get(h, "")) for h in headers]
    _safe_call(ws.append_row, row)
    return data


def update_row(sheet_name: str, row_id: int, data: dict):
    ws = get_sheet(sheet_name)
    headers = _safe_call(ws.row_values, 1)
    records = _safe_call(ws.get_all_records)
    for i, r in enumerate(records):
        if int(r["id"]) == row_id:
            sheet_row = i + 2
            for col_idx, header in enumerate(headers, start=1):
                if header in data:
                    _safe_call(ws.update_cell, sheet_row, col_idx, str(data[header]))
            return True
    return False


def delete_row(sheet_name: str, row_id: int):
    ws = get_sheet(sheet_name)
    records = _safe_call(ws.get_all_records)
    for i, r in enumerate(records):
        if int(r["id"]) == row_id:
            _safe_call(ws.delete_rows, i + 2)
            return True
    return False
