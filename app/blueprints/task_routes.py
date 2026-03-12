from flask import Blueprint, g, request
from ..decorators import require_auth_token
from ..utils import ok
from ..validators import (
    get_json,
    required_str,
    optional_str,
    require_any,
    parse_keyword,
    parse_pagination,
    parse_sorting,
    validate_task_status
)
from ..services.task_service import (
    create_task,
    get_task,
    list_tasks_paginated,
    update_task,
    delete_task
)
bp = Blueprint("tasks", __name__)

@bp.post("/projects/<int:project_id>/tasks")
@require_auth_token
def create_task_route(project_id: int):
    data = get_json(request)
    title = required_str(data, "title", min_len=1, max_len=1000)
    status = validate_task_status(data, required=False, default_status="todo")
    description = optional_str(data, "description", min_len=0, max_len=5000)
    due_date = optional_str(data, "due_date", min_len=1, max_len=100)
    user_id = g.user["user_id"]
    result = create_task(
        user_id=user_id,
        project_id=project_id,
        title=title,
        status=status,
        description=description,
        due_date=due_date
    )
    return ok(data=result, message="Task created", status=201)

@bp.get("/tasks/<int:task_id>")
@require_auth_token
def get_task_route(task_id: int):
    user_id = g.user["user_id"]
    result = get_task(user_id=user_id, task_id=task_id)
    return ok(data=result, message="Task", status=200)

@bp.get("/projects/<int:project_id>/tasks")
@require_auth_token
def list_tasks_route(project_id: int):
    page, page_size = parse_pagination(request)
    sort, order = parse_sorting(
        request, 
        allowed_fields=("id", "title", "status", "due_date", "created_at")
    )
    keyword = parse_keyword(request, max_len=100)
    user_id = g.user["user_id"]
    result = list_tasks_paginated(
        user_id=user_id, 
        project_id=project_id, 
        page=page, 
        page_size=page_size, 
        sort=sort, 
        order=order,
        keyword=keyword
    )
    return ok(data=result, message="Tasks", status=200)

@bp.patch("/tasks/<int:task_id>")
@require_auth_token
def update_task_route(task_id: int):
    data = get_json(request)
    title = optional_str(data, "title", min_len=1, max_len=1000)
    description = optional_str(data, "description", min_len=0, max_len=5000)
    status = validate_task_status(data, required=False)
    due_date = optional_str(data, "due_date", min_len=1, max_len=100)
    user_id = g.user["user_id"]
    require_any(title, status, description, due_date)
    result = update_task(
        user_id=user_id, 
        task_id=task_id, 
        title=title, 
        status=status, 
        description=description, 
        due_date=due_date
    )

    return ok(data=result, message="Task updated", status=200)

@bp.delete("/tasks/<int:task_id>")
@require_auth_token
def delete_task_route(task_id: int):
    user_id = g.user["user_id"]
    delete_task(user_id=user_id, task_id=task_id)
    return ok(data={"deleted": True}, message="Task deleted", status=200)
