from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
import sheets
from auth import hash_pin, create_token, get_current_user, require_admin

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    name: str
    pin: str


class CreateUserRequest(BaseModel):
    name: str
    pin: str
    is_admin: bool = False


def user_dict(u: dict) -> dict:
    return {
        "id": int(u["id"]),
        "name": u["name"],
        "is_admin": str(u.get("is_admin", "")).lower() == "true",
        "pin_changed": str(u.get("pin_changed", "")).lower() == "true",
    }


@router.get("/users")
def list_users():
    return [{"id": int(u["id"]), "name": u["name"], "is_admin": str(u["is_admin"]).lower() == "true"}
            for u in sheets.all_rows("poker_users")]


@router.post("/login")
def login(req: LoginRequest):
    users = sheets.all_rows("poker_users")
    user = next((u for u in users if u["name"] == req.name), None)
    if not user or user["pin_hash"] != hash_pin(req.pin):
        raise HTTPException(status_code=401, detail="Falscher Name oder PIN")
    return {"token": create_token(int(user["id"])), "user": user_dict(user)}


@router.get("/me")
def me(current_user: dict = Depends(get_current_user)):
    return user_dict(current_user)


@router.post("/users")
def create_user(req: CreateUserRequest, admin: dict = Depends(require_admin)):
    users = sheets.all_rows("poker_users")
    if any(u["name"] == req.name for u in users):
        raise HTTPException(status_code=400, detail="Name bereits vergeben")
    uid = sheets.next_id("poker_users")
    data = {
        "id": uid, "name": req.name, "pin_hash": hash_pin(req.pin),
        "is_admin": str(req.is_admin), "pin_changed": "False",
        "created_at": datetime.utcnow().isoformat()
    }
    sheets.insert_row("poker_users", data)
    return {"id": uid, "name": req.name, "is_admin": req.is_admin}


@router.put("/users/{user_id}/pin")
def change_pin(user_id: int, body: dict, current_user: dict = Depends(get_current_user)):
    if int(current_user["id"]) != user_id and str(current_user.get("is_admin", "")).lower() != "true":
        raise HTTPException(status_code=403, detail="Keine Berechtigung")
    sheets.update_row("poker_users", user_id, {
        "pin_hash": hash_pin(body["new_pin"]),
        "pin_changed": "True"
    })
    return {"ok": True}
