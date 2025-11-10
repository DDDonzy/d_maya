from log.config import logger, DEFAULT_FORMAT

from maya import cmds


__all__ = ["uiMessage"]


class MessageHandler:
    def __init__(self):
        self._is_muted = False
        self.pos = "botLeft"
        self.fade = True
        self.fadeInTime = 100
        self.fadeStayTime = 1000
        self.fadeOutTime = 100

    def show(self, msg, *args, **kwargs):
        """Displays a message in the viewport unless muted."""
        if self._is_muted:
            return
        pos = kwargs.get("pos") or kwargs.get("position") or self.pos
        fade = kwargs.get("fade") or kwargs.get("f") or self.fade
        fadeInTime = kwargs.get("fadeInTime") or kwargs.get("fit") or self.fadeInTime
        fadeStayTime = kwargs.get("fadeStayTime") or kwargs.get("fst") or self.fadeStayTime
        fadeOutTime = kwargs.get("fadeOutTime") or kwargs.get("fot") or self.fadeOutTime

        cmds.inViewMessage(
            amg=msg,
            pos=pos,
            fade=fade,
            fadeInTime=fadeInTime,
            fadeStayTime=fadeStayTime,
            fadeOutTime=fadeOutTime,
        )

    def mute(self, mute_status: bool = None):
        """Sets the mute status."""
        if mute_status:
            self._is_muted = mute_status
        else:
            self._is_muted = not self._is_muted

    def is_muted(self):
        """Returns the current mute status."""
        return self._is_muted


ui_maya = False
try:
    ui_maya = not cmds.about(batch=True)
except Exception:
    pass

LEVEL_COLORS = {
    "TRACE": "#29b8db",  # Grey
    "DEBUG": "#3b8eea",  # Light Grey
    "INFO": "#e5e5e5",  # White
    "SUCCESS": "#23d18b",  # Green
    "WARNING": "#f5f543",  # Amber/Orange
    "ERROR": "#f14c4c",  # Red
    "CRITICAL": "#f14c4c",  # Dark Red
}

uiMessage = MessageHandler()


# Maya inViewMessage
if ui_maya:

    def popup_sink(message):
        level_name = message.record["level"].name
        log_message = message.record["message"]
        if level_name in ("INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"):
            color = LEVEL_COLORS.get(level_name, "#FFFFFF")
            msg = f'<font color="{color}">{level_name}: {log_message}</font>'
            uiMessage.show(msg)

    logger.add(
        popup_sink,
        level="INFO",
        format=DEFAULT_FORMAT,
    )

if __name__ == "__main__":
    uiMessage.show("This is a test message!", pos="topCenter", fade=True, fadeStayTime=2000)
