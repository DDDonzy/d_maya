import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma


class UndoCallback(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args):
        cmds.undoInfo(openChunk=True)
        try:
            return self.func(*self.args, **self.kwargs)
        finally:
            cmds.undoInfo(closeChunk=True)


class SkinTool(oma.MFnSkinCluster):
    def __init__(self, skinNodeName):
        sel = om.MSelectionList().add(skinNodeName)
        oma.MFnSkinCluster.__init__(self, sel.getDependNode(0))
        self.skinNodeName = skinNodeName

    def getSkinWeights(self, influenceIndex):

        shapes = cmds.skinCluster(self.skinNodeName, q=True, g=True)
        sel = om.MSelectionList().add(shapes[0])
        path = sel.getDagPath(0)

        singleIdComp = om.MFnSingleIndexedComponent()
        vertexComp = singleIdComp.create(om.MFn.kMeshVertComponent)

        weightData = self.getWeights(path, vertexComp, influenceIndex)
        return weightData


class SeparateBlendshape:
    def __init__(self):
        self.win_name = "separateBlendshape_ui"

    def showUI(self):
        if cmds.window(self.win_name, q=True, ex=True):
            cmds.deleteUI(self.win_name)

        win = cmds.window(self.win_name, title="SeparateBS by Skin ", wh=[400, 180], s=False)
        cmds.columnLayout(adj=True, rs=5, p=win)

        cmds.separator(h=10, style="none")
        self.skin_grp = cmds.textFieldButtonGrp(label="Skin Mesh:", bl="Load", adj=2, bc=self.load_sel_skin)
        self.target_grp = cmds.textFieldButtonGrp(label="Target Mesh:", bl="Load", adj=2, bc=self.load_sel_target)

        cmds.separator(h=5)
        is_maya_2022 = int(cmds.about(q=True, v=True)) >= 2022
        self.use_new_method = cmds.checkBox(label="Use 2022+ Node Method (falloffEval)", v=is_maya_2022)

        cmds.separator(h=10)
        cmds.button(l="Separate", h=40, bgc=[0.36, 0.45, 0.36], c=UndoCallback(self.execute))

        cmds.showWindow(win)

    def load_sel_skin(self):
        sel = cmds.ls(sl=True)
        if sel:
            cmds.textFieldButtonGrp(self.skin_grp, e=True, text=sel[0])

    def load_sel_target(self):
        sel = cmds.ls(sl=True)
        if sel:
            cmds.textFieldButtonGrp(self.target_grp, e=True, text=sel[0])

    def execute(self, *args):
        skin_mesh = cmds.textFieldButtonGrp(self.skin_grp, q=True, text=True)
        target_mesh = cmds.textFieldButtonGrp(self.target_grp, q=True, text=True)
        use_node_method = cmds.checkBox(self.use_new_method, q=True, v=True)

        if not skin_mesh or not target_mesh:
            om.MGlobal.displayError("Please load both meshes.")
            return

        if use_node_method:
            if int(cmds.about(q=True, v=True)) < 2022:
                om.MGlobal.displayError("New method requires Maya 2022 or higher.")
                return

            try:
                import m_utils.deform.bs.split_bs_maya2022 as split
                from importlib import reload

                reload(split)

                split.split_sculpt_by_skin(skin_mesh, target_mesh)
                om.MGlobal.displayInfo("Separation completed using Node Method.")
            except ImportError:
                om.MGlobal.displayError("Script 'split_bs_maya2022' not found in path.")
        else:
            self.old_logic_optimized(skin_mesh, target_mesh)

    def old_logic_optimized(self, skin_mesh, target_mesh):
        """优化后的旧逻辑：减少重复复制，加快属性设置速度"""
        skin_node_name = self.get_skin_cluster(skin_mesh)
        if not skin_node_name:
            om.MGlobal.displayError("No skinCluster found on skin mesh.")
            return

        skin_tool = SkinTool(skin_node_name)
        inf_list = cmds.skinCluster(skin_node_name, q=True, inf=True)
        vtx_count = cmds.polyEvaluate(skin_mesh, v=True)

        base_copy = cmds.duplicate(skin_mesh, name="temp_base_split")[0]

        for i, inf in enumerate(inf_list):
            inf_idx = inf_list.index(inf)
            weights = skin_tool.getSkinWeights(inf_idx)

            res_mesh = cmds.duplicate(base_copy, name="split_{}_Target".format(inf.split(":")[-1]))[0]

            bs = cmds.blendShape(target_mesh, res_mesh, name="tmp_bs")[0]
            cmds.setAttr(bs + "." + target_mesh, 1)

            attr_path = "{}.inputTarget[0].inputTargetGroup[0].targetWeights".format(bs)
            cmds.setAttr("{}[0:{}]".format(attr_path, vtx_count - 1), *weights)

            cmds.delete(res_mesh, ch=True)
            om.MGlobal.displayInfo("Created: {}".format(res_mesh))

        cmds.delete(base_copy)

    def get_skin_cluster(self, mesh):
        rel = cmds.listRelatives(mesh, s=True, f=True)
        if not rel:
            return None
        history = cmds.listHistory(rel[0], pdo=True) or []
        for node in history:
            if cmds.nodeType(node) == "skinCluster":
                return node
        return None


ui = SeparateBlendshape()
ui.showUI()
