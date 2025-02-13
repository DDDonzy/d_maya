from face.ui import ui_main
from face.fn.checkMayaPlugin import checkPlugin


def show_UI():
    checkPlugin()
    ui_main.show_UI()


if __name__ == "__main__":
    show_UI()
