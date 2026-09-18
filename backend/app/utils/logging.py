import logging
import sys


def configure_logging(app):
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '{"level":"%(levelname)s","logger":"%(name)s","message":"%(message)s"}'
    )
    handler.setFormatter(formatter)
    app.logger.handlers.clear()
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
