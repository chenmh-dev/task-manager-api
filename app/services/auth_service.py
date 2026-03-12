from flask import request
from ..db import get_db
from ..exceptions import  LoginFailed, UserExists
from werkzeug.security import generate_password_hash, check_password_hash
from ..auth import generate_auth_token

def register_service(username: str, password: str):
    db = get_db()
    row = db.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    if row:
        raise UserExists()
    
    password_hash = generate_password_hash(password)
    cur = db.execute(
        "INSERT INTO users (username, password) VALUES(?, ?)",
        (username, password_hash)
    )
    db.commit()
    user_id = cur.lastrowid
    return {"user_id": user_id, "username": username}

def login_service(username: str, password: str):
    db = get_db()
    row = db.execute(
        "SELECT id, username, password FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    if not row:
        raise LoginFailed()
    if not check_password_hash(row["password"], password):
        raise LoginFailed()
    token = generate_auth_token({"user_id": row["id"]})

    return {"user_id": row["id"], "username": row["username"], "token": token}
