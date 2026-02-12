import z_bs.ui.uiMain as bsUI
from z_bs._tools import debugUI
from importlib import reload


if __name__ == "__main__":
    ui = bsUI.ShapeToolsWidget()
    ui.show()

    # debugUI=  _debugUI.WidgetDebugTool(ui)
    # debugUI.show()


# TODO
# head_lod0_mesh__mouth_dimple_left --->>>  head_lod0_mesh__mouth_dimple_right  无法反转or镜像
# matehuman  lod0  级别数量，mirror / flip 速度太慢了wq
