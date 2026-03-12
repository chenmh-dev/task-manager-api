from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import current_app

def _get_auth_token_serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="auth-token")

def generate_auth_token(payload: dict) -> str:
    s = _get_auth_token_serializer()
    return s.dumps(payload)

def verify_auth_token(token: str, max_age_seconds: int = 3600) -> dict | None:
    s = _get_auth_token_serializer()
    try:
        data = s.loads(token, max_age=max_age_seconds)
        return data
    except (BadSignature, SignatureExpired):
        return None
