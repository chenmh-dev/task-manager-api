from flask import Blueprint, request, g
from ..decorators import require_auth_token
from ..utils import ok
from ..services.project_service import (
    create_project,
    list_projects_paginated,
    get_project,
    update_project,
    delete_project,
)
from ..validators import (
    get_json,
    required_str,
    optional_str,
    parse_keyword,
    parse_pagination,
    parse_sorting,
    require_any,
)

bp = Blueprint("projects", __name__)


@bp.post("/projects")
@require_auth_token
def create_project_route():
    payload = get_json(request)
    name = required_str(payload, "name", min_len=1, max_len=200)
    description = optional_str(payload, "description", min_len=0, max_len=2000)

    user_id = g.user["user_id"]
    result = create_project(user_id=user_id, name=name, description=description)
    return ok(data=result, message="Project created", status=201)


@bp.get("/projects")
@require_auth_token
def list_projects_route():
    page, page_size = parse_pagination(request, default_page=1, default_page_size=10, max_page_size=50)
    sort, order = parse_sorting(
        request,
        allowed_fields=("id", "name", "created_at"),
        default_field="id",
        default_order="desc"
    )
    keyword = parse_keyword(request, max_len=100)

    user_id = g.user["user_id"]
    result = list_projects_paginated(
        user_id=user_id,
        page=page,
        page_size=page_size,
        sort=sort,
        order=order,
        keyword=keyword,
    )
    return ok(data=result, message="Projects", status=200)


@bp.get("/projects/<int:project_id>")
@require_auth_token
def get_project_route(project_id: int):
    user_id = g.user["user_id"]
    result = get_project(user_id=user_id, project_id=project_id)
    return ok(data=result, message="Project", status=200)


@bp.patch("/projects/<int:project_id>")
@require_auth_token
def update_project_route(project_id: int):
    payload = get_json(request)
    name = optional_str(payload, "name", min_len=1, max_len=200)
    description = optional_str(payload, "description", min_len=0, max_len=2000)
    require_any(name, description)

    user_id = g.user["user_id"]
    result = update_project(
        user_id=user_id,
        project_id=project_id,
        name=name,
        description=description,
    )
    return ok(data=result, message="Project updated", status=200)


@bp.delete("/projects/<int:project_id>")
@require_auth_token
def delete_project_route(project_id: int):
    user_id = g.user["user_id"]
    delete_project(user_id=user_id, project_id=project_id)
    return ok(data={"deleted": True}, message="Project deleted", status=200)