import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging(app):
    log_dir = Path(app.root_path).parent / "logs"
    log_dir.mkdir(exist_ok=True)

    handler = RotatingFileHandler(
        filename=log_dir / "app.log",
        maxBytes=2_000_000,
        backupCount=3,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s request_id=%(request_id)s %(message)s"
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    # Flask 默认 logger：app.logger
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    # 避免重复输出（Windows/调试模式下常见）
    app.logger.propagate = False