from pathlib import Path
from maya import cmds
import numpy as np
import z_np._reload as reload
import z_np.src.cWeightsHandle as cWeightsHandle
import z_np.convert as convert

test_file = Path(r"C:/Users/Donzy/Desktop/cWeights_file.ma")
plugin_path = Path(r"E:\d_maya\z_np\cSkin.py")
reload.reload_modules_in_path(r"E:\d_maya\z_np")

plugin_name = plugin_path.name


cmds.file(new=True, force=True)


if cmds.pluginInfo(plugin_name, q=True, loaded=True):
    cmds.unloadPlugin(plugin_name)


cmds.loadPlugin(plugin_path)
print(f"Plugin {plugin_name} reloaded successfully!")

cmds.file(test_file, o=1, f=1)


if __name__ == "__main__":
    sk = "skinCluster1"
    deformer = "cSkinDeformer1"

    print("Running Maya test script...")

    cmds.setAttr("cSkinDeformer1.cWeightsLayers[0].cWeightsLayerEnabled", 1)
    cmds.setAttr("cSkinDeformer1.cWeightsLayers[1].cWeightsLayerEnabled", 1)

    wManager = cWeightsHandle.CSkinWeightManager(deformer)

    w = list(convert.get_skinWeights(sk)[0])
    wManager.layers[1]["weights"].set_weights(w)
    
    wManager.layers[0]["mask"].resize(385)
    wManager.layers[0]["mask"].fill_with_value(1)
    wManager.layers[1]["mask"].resize(385)
    wManager.layers[1]["mask"].fill_with_value(1)
