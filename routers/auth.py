"""Router for authentication — /auth/signup, /auth/login, /auth/me.
Supports teacher and student roles.
"""

import hashlib
import json
import secrets
from pathlib import Path
from typing import Dict, Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

USERS_FILE = Path(__file__).parent.parent / "users.json"
_tokens: Dict[str, dict] = {}   # token → {username, role}


def _load_users() -> dict:
    if USERS_FILE.exists():
        raw = json.loads(USERS_FILE.read_text())
        # Migrate old flat format {username: hash} → new format
        migrated = {}
        for k, v in raw.items():
            if isinstance(v, str):
                migrated[k] = {"hash": v, "role": "student"}
            else:
                migrated[k] = v
        return migrated
    return {}


def _save_users(users: dict) -> None:
    USERS_FILE.write_text(json.dumps(users, indent=2))


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _seed_admin() -> None:
    """Ensure the hardcoded teacher account (admin / admin@123) always exists."""
    users = _load_users()
    if "admin" not in users:
        users["admin"] = {"hash": _hash("admin@123"), "role": "teacher"}
        _save_users(users)


_seed_admin()


# ── Schemas ────────────────────────────────────────────────────────────────
class SignupRequest(BaseModel):
    username: str
    password: str
    role: Literal["teacher", "student"] = "student"


class LoginRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    token: str
    username: str
    role: str


# ── Endpoints ──────────────────────────────────────────────────────────────
@router.post("/signup", response_model=AuthResponse)
def signup(req: SignupRequest) -> AuthResponse:
    users = _load_users()
    if req.username in users:
        raise HTTPException(status_code=409, detail="Username already taken.")
    users[req.username] = {"hash": _hash(req.password), "role": req.role}
    _save_users(users)
    token = secrets.token_hex(32)
    _tokens[token] = {"username": req.username, "role": req.role}
    return AuthResponse(token=token, username=req.username, role=req.role)


@router.post("/login", response_model=AuthResponse)
def login(req: LoginRequest) -> AuthResponse:
    users = _load_users()
    user = users.get(req.username)
    if not user or user["hash"] != _hash(req.password):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    token = secrets.token_hex(32)
    role = user.get("role", "student")
    _tokens[token] = {"username": req.username, "role": role}
    return AuthResponse(token=token, username=req.username, role=role)


@router.get("/me")
def me(token: str) -> dict:
    info = _tokens.get(token)
    if not info:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    return {"username": info["username"], "role": info["role"]}
