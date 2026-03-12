from ..db import get_db
from ..exceptions import NotFound, BadRequest

def _ensure_project_owned(user_id: int, project_id: int) -> None:
    db = get_db()
    row = db.execute(
        "SELECT id FROM projects WHERE id = ? AND owner_id = ?",
        (project_id, user_id)
    ).fetchone()
    if row is None:
        raise NotFound(code="PROJECT_NOT_FOUND", message="Project not found")

def create_task(
    user_id: int, 
    project_id: int,
    title: str,
    status: str,
    description: str | None,
    due_date: str | None
) -> dict:
    _ensure_project_owned(user_id=user_id, project_id=project_id)

    db = get_db()

    cur = db.execute(
        "INSERT INTO tasks (project_id, title, description, status, due_date) VALUES (?, ?, ?, ?, ?)",
        (project_id, title, description, status, due_date)
    )
    db.commit()
    task_id = cur.lastrowid
    return get_task(user_id=user_id, task_id=task_id)

def get_task(user_id: int, task_id: int) -> dict:
    db = get_db()
    row = db.execute("""
        SELECT t.* 
        FROM tasks t 
        JOIN projects p ON t.project_id = p.id 
        WHERE t.id = ? AND p.owner_id = ?""",
        (task_id, user_id)
    ).fetchone()
    if row is None:
        raise NotFound(code="TASK_NOT_FOUND", message="Task not found")
    
    return dict(row)

def list_tasks_paginated(
    user_id: int, 
    project_id: int, 
    page: int, 
    page_size: int, 
    sort: str, 
    order: str,
    keyword: str | None
) -> dict:
    _ensure_project_owned(user_id=user_id, project_id=project_id)
    
    db = get_db()
    where_clause = "WHERE project_id = ? "
    params = [project_id]

    if keyword:
        where_clause += f"AND title LIKE ? "
        params.append(f"%{keyword}%")

    total_row = db.execute("""
        SELECT COUNT(*) as count 
        FROM tasks """ + where_clause,
        tuple(params)
    ).fetchone()
    total = total_row["count"]
    total_pages = (total + page_size - 1) // page_size

    query = (f"""
        SELECT id, title, description, status, due_date, created_at
        FROM tasks
        {where_clause}
        ORDER BY {sort} {order}
        LIMIT ? OFFSET ?
    """)
    offset = (page - 1) * page_size
    rows = db.execute(
        query,
        tuple(params + [page_size, offset])
    ).fetchall()
    items = [dict(r) for r in rows]

    return {
        "items": items,
        "pagination":{
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages
        }
    }

def update_task(
    user_id: int, 
    task_id: int,
    title: str | None,
    status: str | None,
    description: str | None,
    due_date: str | None
) -> dict:
    db = get_db()
    updates = []
    params = []

    if title is not None:
        updates.append("title = ?")
        params.append(title)

    if description is not None:
        updates.append("description = ?")
        params.append(description)

    if due_date is not None:
        updates.append("due_date = ?")
        params.append(due_date)
    
    if status is not None:
        updates.append("status = ?")
        params.append(status)

    if not updates:
        raise BadRequest(message="no fields to update")

    cur = db.execute(f"""
        UPDATE tasks
        SET {', '.join(updates)}
        WHERE id = ? AND project_id IN (
            SELECT id FROM projects WHERE owner_id = ?
        )
        """,
        tuple(params + [task_id, user_id])
    )
    db.commit()
    if cur.rowcount == 0:
        raise NotFound(code="TASK_NOT_FOUND", message="Task not found")
    

    return get_task(user_id=user_id, task_id=task_id)

def delete_task(user_id: int, task_id: int) -> None:
    db = get_db()
    cur = db.execute("""
        DELETE FROM tasks
        WHERE id = ? AND project_id IN(
            SELECT id FROM projects WHERE owner_id = ?
        )
        """,
        (task_id, user_id)
    )
    db.commit()
    if cur.rowcount == 0:
        raise NotFound(code="TASK_NOT_FOUND", message="Task not found")
    



