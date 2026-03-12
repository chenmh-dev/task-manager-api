class AppError(Exception):
    def __init__(self, code: str, message: str, status: int, extra: dict | None = None):
        self.code = code
        self.message = message
        self.status = status
        self.extra = extra or {}

class BadRequest(AppError):
    def __init__(self, code="BAD_REQUEST", message="Bad Request", extra = None):
        super().__init__(code=code, message=message, status=400, extra=extra)

class Unauthorized(AppError):
    def __init__(self, code="UNAUTHORIZED", message="Unauthorized", extra = None):
        super().__init__(code=code, message=message, status=401, extra=extra)

class Forbidden(AppError):
    def __init__(self, code="FORBIDDEN", message="Forbidden", extra = None):
        super().__init__(code=code, message=message, status=403, extra=extra)

class NotFound(AppError):
    def __init__(self, code="NOT_FOUND", message="Not found", extra = None):
        super().__init__(code=code, message=message, status=404, extra=extra)

class Conflict(AppError):
    def __init__(self, code="CONFLICT", message="Conflict", extra = None):
        super().__init__(code=code, message=message, status=409, extra=extra)

class LoginFailed(Unauthorized):
    def __init__(self, code="LOGIN_FAILED", message="Invalid username or password", extra = None):
        super().__init__(code=code, message=message, extra=extra)

class UserExists(Conflict):
    def __init__(self, code="USER_EXISTS", message="username already exists", extra=None):
        super().__init__(code=code, message=message, extra=extra)