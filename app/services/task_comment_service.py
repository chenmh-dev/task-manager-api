from ..db import get_db
from ..exceptions import NotFound, BadRequest

ALLOWED_TASK_COMMENT_SORT_FIELDS = ("id", "created_at", "user_id")
ALLOWED_SORT_ORDERS = ("asc", "desc")


def _ensure_task_owned(user_id: int, task_id: int) -> None:
    db = get_db()
    row = db.execute(
        """
        SELECT t.id
        FROM tasks t
        JOIN projects p ON t.project_id = p.id
        WHERE t.id = ? AND p.owner_id = ?
        """,
        (task_id, user_id),
    ).fetchone()

    if row is None:
        raise NotFound(code="TASK_NOT_FOUND", message="Task not found")


def create_task_comment(user_id: int, task_id: int, content: str) -> dict:
    _ensure_task_owned(user_id=user_id, task_id=task_id)

    db = get_db()
    cur = db.execute(
        "INSERT INTO task_comments (task_id, user_id, content) VALUES (?, ?, ?)",
        (task_id, user_id, content),
    )
    db.commit()

    task_comment_id = cur.lastrowid

    return {
        "id": task_comment_id,
        "task_id": task_id,
        "user_id": user_id,
        "content": content,
    }


def list_task_comments_paginated(
    user_id: int,
    task_id: int,
    page: int,
    page_size: int,
    sort: str,
    order: str,
    keyword: str | None,
) -> dict:
    _ensure_task_owned(user_id=user_id, task_id=task_id)

    if sort not in ALLOWED_TASK_COMMENT_SORT_FIELDS:
        raise BadRequest(message="invalid sort field")
    if order not in ALLOWED_SORT_ORDERS:
        raise BadRequest(message="invalid sort order")

    db = get_db()
    where_clause = "WHERE task_id = ? "
    params = [task_id]

    if keyword:
        where_clause += "AND content LIKE ? "
        params.append(f"%{keyword}%")

    total_row = db.execute(
        f"""
        SELECT COUNT(*) AS count
        FROM task_comments
        {where_clause}
        """,
        tuple(params),
    ).fetchone()
    total = total_row["count"]
    total_pages = (total + page_size - 1) // page_size

    query = f"""
        SELECT id, task_id, user_id, content, created_at
        FROM task_comments
        {where_clause}
        ORDER BY {sort} {order}
        LIMIT ? OFFSET ?
    """

    offset = (page - 1) * page_size
    rows = db.execute(
        query,
        tuple(params + [page_size, offset]),
    ).fetchall()

    items = [dict(r) for r in rows]

    return {
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
        },
    }


def delete_task_comment(user_id: int, task_comment_id: int) -> None:
    db = get_db()
    cur = db.execute(
        "DELETE FROM task_comments WHERE id = ? AND user_id = ?",
        (task_comment_id, user_id),
    )

    if cur.rowcount == 0:
        raise NotFound(code="TASK_COMMENT_NOT_FOUND", message="Task comment not found")

    db.commit()