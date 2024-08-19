# Author:   Donzy.xu
# CreateTime:   2023/3/19 - 17:52
# FileName:  main.py
import sys
import os
if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))

import UI.run_Maya2017 as ui
win = ui.Ui_RigTools()

if __name__ == "__main__":
    win = ui.Ui_RigTools()
