import os
import sys
from importlib import reload

path = r"E:/d_maya"
if path not in sys.path:
    sys.path.append(path)


def reload_modules_in_path(path):
    reload_list = []
    for modules_name in sys.modules:
        try:
            modules_path = sys.modules[modules_name].__file__
            common_path = os.path.commonpath([path, modules_path])
            if os.path.samefile(path, common_path):
                reload_list.append(sys.modules[modules_name])
        except:
            pass
    for x in reload_list:
        reload(x)
        print(f"Reload: {x}")


# reload_modules_in_path(path)
