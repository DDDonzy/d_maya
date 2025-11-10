from log.config import logger, debug, info, warning, error, critical, exception, catch, success, trace

try:
    from log.logInViewMessage import uiMessage  # noqa: F401
except Exception as e:
    print(e)


__all__ = [
    "logger",
    "debug",
    "info",
    "warning",
    "error",
    "critical",
    "exception",
    "catch",
    "success",
    "trace",
]
