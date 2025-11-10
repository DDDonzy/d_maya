from log.config import logger, debug, info, warning, error, critical, exception, catch, success, trace, set_level


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
    "set_level",
]

try:
    from log.logInViewMessage import uiMessage  # noqa: F401

    __all__.append("uiMessage")
except Exception:
    pass
