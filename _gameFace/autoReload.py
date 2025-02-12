import os
import sys
from imp import reload

path = os.path.dirname(__file__)

def reloadALL(path=path):
    """Reload all modules in the specified path."""
    reload_list = []
    for modules_name in sys.modules:
        try:
            modules_path = sys.modules[modules_name].__file__
            common_path = os.path.commonprefix([os.path.abspath(path), os.path.abspath(modules_path)])
        except:
            continue
        if os.path.abspath(modules_path).startswith(os.path.abspath(path)):
            reload_list.append(sys.modules[modules_name])
    for x in reload_list:
        reload(x)
        print("Reload: {}".format(x))

if __name__ == "__main__":
    reloadALL(path)