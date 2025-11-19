from functools import partial

from log.config import logger, level_filter, DEFAULT_FORMAT
from log.mayaScriptLineColor import ScriptEditorStyler

from maya import cmds, utils

__all__ = ["uiMessage"]


class MessageHandler:
    def __init__(self):
        self._message_list = []
        self._job_scheduled = False

        self._is_muted = False
        self.pos = "botLeft"
        self.fade = True
        self.fadeInTime = 100
        self.fadeStayTime = 1000
        self.fadeOutTime = 100

    def _show_messages(self):
        if not self._message_list:
            self._job_scheduled = False
            return

        self._job_scheduled = False

        for showMessage_command in self._message_list:
            try:
                showMessage_command()
            except Exception:
                pass
        self._message_list.clear()

    def show(self, msg, *args, **kwargs):
        """Displays a message in the viewport unless muted."""
        if self._is_muted:
            return
        pos = kwargs.get("pos") or kwargs.get("position") or self.pos
        fade = kwargs.get("fade") or kwargs.get("f") or self.fade
        fadeInTime = kwargs.get("fadeInTime") or kwargs.get("fit") or self.fadeInTime
        fadeStayTime = kwargs.get("fadeStayTime") or kwargs.get("fst") or self.fadeStayTime
        fadeOutTime = kwargs.get("fadeOutTime") or kwargs.get("fot") or self.fadeOutTime

        showMessage_command = partial(
            cmds.inViewMessage,
            amg=msg,
            pos=pos,
            fade=fade,
            fadeInTime=fadeInTime,
            fadeStayTime=fadeStayTime,
            fadeOutTime=fadeOutTime,
        )
        self._message_list.append(showMessage_command)
        if len(self._message_list) > 3:
            self._message_list.pop(0)

        if not self._job_scheduled:
            self._job_scheduled = True
            utils.executeDeferred(self._show_messages)

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
    "TRACE": "#29b8db",
    "DEBUG": "#3b8eea",
    "INFO": "#e5e5e5",
    "NOTICE": "#b0b0b0",
    "SUCCESS": "#23d18b",
    "WARNING": "#f5f543",
    "ERROR": "#f14c4c",
}

uiMessage = MessageHandler()
scriptStyler = ScriptEditorStyler()


# Maya inViewMessage
def popup_sink(message):
    level_name = message.record["level"].name
    log_message = message.record["message"]
    color = LEVEL_COLORS.get(level_name, "#FFFFFF")
    msg = f'<font color="{color}">{level_name}: {log_message}</font>'
    scriptStyler.update(level_name)
    uiMessage.show(msg)


# Maya inViewMessage format
def maya_inViewMessage_formatter(record):
    """Custom formatter to handle multi-line messages."""
    record["message"] = record["message"].strip()
    return DEFAULT_FORMAT


MAYA_CONSOLE_ID = None
if ui_maya:
    MAYA_CONSOLE_ID = logger.add(
        popup_sink,
        level="INFO",
        filter=level_filter,
        format=maya_inViewMessage_formatter,
    )

if __name__ == "__main__":
    uiMessage.show("This is a test message!", pos="topCenter", fade=True, fadeStayTime=2000)
