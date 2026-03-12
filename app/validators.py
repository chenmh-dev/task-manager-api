from typing import Any


from .exceptions import BadRequest


def get_json(request) -> dict:
    data = request.get_json(silent=True)

    if data is None:
        raise BadRequest(message="Invalid json body")

    if not isinstance(data, dict):
        raise BadRequest(message="Json body must be an object")

    return data


def required_str(
    data: dict,
    key: str,
    *,
    min_len: int = 1,
    max_len: int = 2000,
) -> str:
    val = data.get(key)

    if val is None:
        raise BadRequest(message=f"{key} is required")

    if not isinstance(val, str):
        raise BadRequest(message=f"{key} must be a string")

    s = val.strip()

    if len(s) < min_len:
        raise BadRequest(message=f"{key} is too short")

    if len(s) > max_len:
        raise BadRequest(message=f"{key} is too long")

    return s


def optional_str(
    data: dict,
    key: str,
    *,
    min_len: int = 1,
    max_len: int = 2000,
) -> str | None:
    val = data.get(key)

    if val is None:
        return None

    if not isinstance(val, str):
        raise BadRequest(message=f"{key} must be a string")

    s = val.strip()

    if len(s) < min_len:
        raise BadRequest(message=f"{key} is too short")

    if len(s) > max_len:
        raise BadRequest(message=f"{key} is too long")

    return s


def require_any(*values: Any, message: str = "no fields to update") -> None:
    if all(v is None for v in values):
        raise BadRequest(message=message)


def parse_pagination(
    request,
    *,
    default_page: int = 1,
    default_page_size: int = 10,
    max_page_size: int = 50,
) -> tuple[int, int]:
    page_raw = request.args.get("page", str(default_page))
    page_size_raw = request.args.get("page_size", str(default_page_size))

    try:
        page = int(page_raw)
        page_size = int(page_size_raw)
    except ValueError:
        raise BadRequest(message="page and page_size must be integers")

    if page < 1:
        raise BadRequest(message="page must be >= 1")

    if page_size < 1 or page_size > max_page_size:
        raise BadRequest(message=f"page_size must be between 1 and {max_page_size}")

    return page, page_size


def parse_sorting(
    request,
    *,
    allowed_fields: tuple[str, ...],
    default_field: str = "id",
    default_order: str = "desc",
) -> tuple[str, str]:
    sort = request.args.get("sort", default_field)
    order = request.args.get("order", default_order).lower()

    if sort not in allowed_fields:
        raise BadRequest(message=f"sort must be one of {list(allowed_fields)}")

    if order not in ("asc", "desc"):
        raise BadRequest(message="order must be 'asc' or 'desc'")

    return sort, order


def parse_keyword(request, max_len: int = 100) -> str | None:
    keyword = request.args.get("keyword")

    if keyword is None:
        return None

    keyword = str(keyword).strip()

    if len(keyword) > max_len:
        raise BadRequest(message="keyword is too long")

    return keyword if keyword else None

def validate_task_status(
    data: dict, 
    required: bool = True,
    default_status: str | None = None,
    default_status_fields: tuple[str, ...] = ("todo", "in_progress", "done")
) -> str | None:
    val = data.get("status", None)

    if not isinstance(val, str):
        raise BadRequest(message="status must be a string")
    
    if val is None:
        if required:
            raise BadRequest(message="status is required")
        else:
            return default_status
    
    status = val.strip().lower()
    if status not in default_status_fields:
        raise BadRequest(message=f"status must be one of {list(default_status_fields)}")
    return status




