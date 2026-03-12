from flask import Blueprint, g
from ..db import get_db
from ..decorators import require_auth_token
from ..exceptions import NotFound
from ..utils import ok

bp = Blueprint("user", __name__)

@bp.get("/me")
@require_auth_token
def me():
    user_id = g.user["user_id"]
    db = get_db()
    row = db.execute(
        "SELECT id, username, created_at FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    if not row:
        raise NotFound(code="USER_NOT_FOUND", message="User not found")
    
    return ok(
        data={
            "id": row["id"], 
            "username": row["username"],
            "created_at": row["created_at"]
        }, 
        message="Me", 
        status=200
    )
