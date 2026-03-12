import time, uuid, os
from flask import Flask, g, request
from .errors import register_error_handler
from .logging_utils import setup_logging
from .db import init_db, close_db
from .config import DevelopmentConfig, ProductionConfig
def created_app():
    app = Flask(__name__)
    
    env = os.getenv("APP_ENV", "development").lower()
    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    setup_logging(app)

    init_db()

    @app.before_request
    def _start_timer_and_request_id():
        g.start_time = time.time()
        g.request_id = uuid.uuid4().hex[:12]

    @app.after_request
    def _log_request(response):
        duration_ms = int((time.time() - getattr(g, "start_time", time.time()))*1000)
        user_id = None
        if hasattr(g, "user") and isinstance(g.user, dict):
            user_id = g.user.get("user_id")
        
        response.headers["X-Request-Id"] = g.request_id

        app.logger.info(
            f'{request.method} {request.path} status={response.status_code} '
            f'duration_mc={duration_ms} user_id={user_id}',
            extra={"request_id": g.request_id}
        )
        return response

    app.teardown_appcontext(close_db)

    from .routes import bp as home
    from .blueprints.auth_routes import bp as auth
    from .blueprints.user_routes import bp as user
    from .blueprints.project_routes import bp as project
    from .blueprints.task_routes import bp as task
    from .blueprints.task_comment_routes import bp as task_comment

    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(project)
    app.register_blueprint(task)
    app.register_blueprint(task_comment)

    register_error_handler(app)
    
    return app