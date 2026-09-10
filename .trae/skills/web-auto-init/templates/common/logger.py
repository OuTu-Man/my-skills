import logging
import os
import re
import sys

from loguru import logger
from loguru._defaults import env as logger_env


def init_logger(env: str, start_dt: str):
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel("DEBUG")

    fmt = logger_env(
        "LOGURU_FORMAT",
        str,
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "{thread.name} - <level>{extra[obfuscated_message]}</level> "
        "(<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>) \n",
    )
    patterns = [
        "password",
        "secret_key",
        "2fa",
        "2fa_code",
        "token",
        "otp_secret",
    ]

    def obfuscate_message(message: str):
        """Obfuscate sensitive information."""
        msg = message
        rep_re = r"\g<key_name>\g<mark>\g<link>\g<vmark>******\g<vmark>\g<end>"
        for pattern in patterns:
            match_re = (
                r"(?P<key_name>"
                + pattern
                + r")(?P<mark>['\"\\]{0,3})(?P<link>[:=\s]{0,3})"
                + r"(?P<vmark>['\"\\]{0,3})(.+?)(?P=vmark)(?P<end>[,\s]?)"
            )
            msg = re.sub(match_re, rep_re, msg, flags=re.I | re.M)
        return msg

    def formatter(record):
        record["extra"]["obfuscated_message"] = obfuscate_message(record["message"])
        return fmt

    worker_name = os.environ.get("PYTEST_XDIST_WORKER", "")
    worker_suffix = f"main_{worker_name}" if worker_name else f"main_{os.getpid()}"
    log_file = f"logs/{env}_{start_dt}/{worker_suffix}.log"
    os.makedirs("logs", exist_ok=True)

    config = {
        "handlers": [
            {"sink": sys.stderr, "format": formatter},
        ],
    }
    logger.configure(**config)
    logger.remove()
    logger.add(sys.stderr, format=formatter)
    logger.add(log_file, level=logging.DEBUG, retention=5, format=formatter)
    logger.info("init logger complete...")
