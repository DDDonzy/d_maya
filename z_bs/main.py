import z_bs.ui as bsUI
from z_bs._tools import _debugUI
from importlib import reload
reload(bsUI)


ui = bsUI.ShapeToolsWidget()
ui.show()

# debugUI=  _debugUI.WidgetDebugTool(ui)
# debugUI.show()