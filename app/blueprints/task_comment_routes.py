from flask import Blueprint, request, g
from ..decorators import require_auth_token
from ..utils import ok
from ..validators import (
    get_json,
    required_str,
    parse_sorting,
    parse_keyword,
    parse_pagination,
)
from ..services.task_comment_service import (
    create_task_comment,
    list_task_comments_paginated,
    delete_task_comment,
    ALLOWED_TASK_COMMENT_SORT_FIELDS,
)

bp = Blueprint("task_comments", __name__)


@bp.post("/tasks/<int:task_id>/comments")
@require_auth_token
def create_task_comment_route(task_id: int):
    data = get_json(request)
    content = required_str(data, "content", min_len=1, max_len=2000)
    user_id = g.user["user_id"]

    result = create_task_comment(user_id=user_id, task_id=task_id, content=content)
    return ok(data=result, message="Task comment created", status=201)


@bp.get("/tasks/<int:task_id>/comments")
@require_auth_token
def list_task_comments_paginated_route(task_id: int):
    page, page_size = parse_pagination(request)
    sort, order = parse_sorting(
        request,
        allowed_fields=ALLOWED_TASK_COMMENT_SORT_FIELDS,
        default_field="id",
        default_order="desc",
    )
    keyword = parse_keyword(request)
    user_id = g.user["user_id"]

    result = list_task_comments_paginated(
        user_id=user_id,
        task_id=task_id,
        page=page,
        page_size=page_size,
        sort=sort,
        order=order,
        keyword=keyword,
    )
    return ok(data=result, message="Task comments", status=200)


@bp.delete("/task-comments/<int:task_comment_id>")
@require_auth_token
def delete_task_comment_route(task_comment_id: int):
    user_id = g.user["user_id"]
    delete_task_comment(user_id=user_id, task_comment_id=task_comment_id)
    return ok(data={"deleted": True}, message="Task comment deleted", status=200)