from flask import jsonify

def ok(data: dict = None, message: str = "OK", status: int = 200):
    return jsonify({
            "success": True,
            "data": data,
            "message": message,
        }),status

def fail(code: str = "ERROR", message: str = "error", status: int = 500):
    return jsonify({
        "success": False,
        "code": code,
        "message": message
    }), status