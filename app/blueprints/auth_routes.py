from flask import Blueprint, g, request
from ..validators import get_json, required_str
from ..services.auth_service import register_service, login_service
from ..utils import ok
bp = Blueprint("auth", __name__)

@bp.post("/register")
def register_route():
    data = get_json(request)
    username = required_str(data, "username", min_len=1, max_len=100)
    password = required_str(data, "password", min_len=2, max_len=200)
    result = register_service(username=username, password=password)
    return ok(data=result, message="Register success", status=200)

@bp.post("/login")
def login_route():
    data = get_json(request)
    username = required_str(data, "username", min_len=1, max_len=100)
    password = required_str(data, "password", min_len=2, max_len=200)
    result = login_service(username, password)
    return ok(data=result, message="Login success", status=200)
