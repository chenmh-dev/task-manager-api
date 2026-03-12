from flask import Blueprint

bp = Blueprint("route", __name__)
@bp.get("/")
def home_route():
    return "HOME PAGE"