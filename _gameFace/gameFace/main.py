from gameFace.ui import ui_main
from gameFace.fn.checkMayaPlugin import checkPlugin


def show_UI():
    checkPlugin()
    ui_main.show_UI()


if __name__ == "__main__":
    show_UI()
