import os
import sys
from importlib import reload

path = r"E:/d_maya"
if path not in sys.path:
    sys.path.append(path)