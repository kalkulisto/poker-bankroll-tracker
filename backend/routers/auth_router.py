from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db, User
from auth import hash_pin, create_token, get_current_user, require_admin

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    name: str
    pin: str


class CreateUserRequest(BaseModel):
    name: str
    pin: str
    is_admin: bool = False


@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "name": u.name, "is_admin": u.is_admin} for u in users]


@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == req.name).first()
    if not user or user.pin_hash != hash_pin(req.pin):
        raise HTTPException(status_code=401, detail="Falscher Name oder PIN")
    return {
        "token": create_token(user.id),
        "user": {"id": user.id, "name": user.name, "is_admin": user.is_admin}
    }


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "name": current_user.name, "is_admin": current_user.is_admin}


@router.post("/users")
def create_user(req: CreateUserRequest, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    if db.query(User).filter(User.name == req.name).first():
        raise HTTPException(status_code=400, detail="Name bereits vergeben")
    user = User(name=req.name, pin_hash=hash_pin(req.pin), is_admin=req.is_admin)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "name": user.name, "is_admin": user.is_admin}


@router.put("/users/{user_id}/pin")
def change_pin(user_id: int, body: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Keine Berechtigung")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Nicht gefunden")
    user.pin_hash = hash_pin(body["new_pin"])
    db.commit()
    return {"ok": True}
