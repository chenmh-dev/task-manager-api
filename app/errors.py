from werkzeug.exceptions import HTTPException
from .exceptions import AppError
from flask import Flask, g
from .utils import fail

def register_error_handler(app: Flask):
    @app.errorhandler(AppError)
    def hande_app_error(err):
        rid = getattr(g, "request_id", "-")
        app.logger.warning(
            f"AppError code={err.code}, message={err.message}, status={err.status}",
            extra={"request_id": rid}
        )
        return fail(code=err.code, message=err.message, status=err.status)

    @app.errorhandler(HTTPException)
    def handle_unexpected_error(err):
        rid = getattr(g, "request_id", "-")
        app.logger.exception("Unhandled exception", extra={"request_id": rid})
        import traceback
        traceback.print_exc()
        return fail(code="INTERNAL_ERROR", message="Internal server error", status=500)