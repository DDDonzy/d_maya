from maya import cmds


__all__ = ["uiMessage", "showMessage", "muteMessage"]


class MessageHandler:
    def __init__(self):
        self._is_muted = False
        self.pos = "botRight"
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
        fadeOutTime = kwargs.get("fadeOutTime" or kwargs.get("fot")) or self.fadeOutTime

        message = f"<hl> {msg} </hl>"
        cmds.inViewMessage(
            amg=message,
            pos=pos,
            fade=fade,
            fadeInTime=fadeInTime,
            fadeStayTime=fadeStayTime,
            fadeOutTime=fadeOutTime,
        )

    def mute(self, mute_status: bool):
        """Sets the mute status."""
        self._is_muted = mute_status

    def is_muted(self):
        """Returns the current mute status."""
        return self._is_muted


uiMessage = MessageHandler()


def showMessage(msg):
    """只是为了支持旧代码调用"""
    uiMessage.show(msg)


def muteMessage(mute: bool):
    """只是为了支持旧代码调用"""
    uiMessage.mute(mute)
