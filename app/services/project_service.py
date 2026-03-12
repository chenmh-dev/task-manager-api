from ..db import get_db
from ..exceptions import NotFound, BadRequest


def create_project(user_id: int, name: str, description: str | None) -> dict:
    db = get_db()
    cur = db.execute(
        "INSERT INTO projects (owner_id, name, description) VALUES (?, ?, ?)",
        (user_id, name, description),
    )
    db.commit()

    project_id = cur.lastrowid
    return get_project(user_id=user_id, project_id=project_id)


def list_projects_paginated(
    user_id: int,
    page: int,
    page_size: int,
    sort: str,
    order: str,
    keyword: str | None,
) -> dict:
    db = get_db()

    where_clause = "WHERE owner_id = ? "
    params = [user_id]

    if keyword:
        where_clause += "AND name LIKE ? "
        params.append(f"%{keyword}%")

    total_row = db.execute(
        f"SELECT COUNT(*) AS count FROM projects {where_clause}",
        tuple(params),
    ).fetchone()
    total = total_row["count"]
    total_pages = (total + page_size - 1) // page_size

    offset = (page - 1) * page_size

    query = (
        f"SELECT id, owner_id, name, description, created_at "
        f"FROM projects {where_clause} "
        f"ORDER BY {sort} {order} "
        f"LIMIT ? OFFSET ?"
    )

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


def get_project(user_id: int, project_id: int) -> dict:
    db = get_db()
    row = db.execute(
        "SELECT id, owner_id, name, description, created_at "
        "FROM projects WHERE id = ? AND owner_id = ?",
        (project_id, user_id),
    ).fetchone()

    if not row:
        raise NotFound(code="PROJECT_NOT_FOUND", message="Project not found")

    return dict(row)


def update_project(
    user_id: int,
    project_id: int,
    name: str | None,
    description: str | None,
) -> dict:
    db = get_db()

    updates = []
    params = []

    if name is not None:
        updates.append("name = ?")
        params.append(name)

    if description is not None:
        updates.append("description = ?")
        params.append(description)

    if not updates:
        raise BadRequest(message="no fields to update")

    cur = db.execute(
        f"UPDATE projects SET {', '.join(updates)} WHERE id = ? AND owner_id = ?",
        tuple(params + [project_id, user_id]),
    )
    if cur.rowcount == 0:
        raise NotFound(code="PROJECT_NOT_FOUND", message="Project not found")
    db.commit()
    
    return get_project(user_id=user_id, project_id=project_id)


def delete_project(user_id: int, project_id: int) -> None:
    db = get_db()
    cur = db.execute(
        "DELETE FROM projects WHERE id = ? AND owner_id = ?",
        (project_id, user_id),
    )
    db.commit()

    if cur.rowcount == 0:
        raise NotFound(code="PROJECT_NOT_FOUND", message="Project not found")