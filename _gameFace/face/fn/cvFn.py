import yaml
from maya import mel, cmds
from maya.api import OpenMaya as om
from face.fn.showMessage import showMessage
from face.fn.mirrorEnv import MIRROR_CONFIG
from face.fn.choseFile import choseFile


class CurveShapeData(yaml.YAMLObject):
    yaml_tag = 'CurveShapeData'

    def __init__(self, shapeName="shapeName", lineWidth=0, overrideEnabled=False, overrideRGBColors=False, hideOnPlayback=False, overrideColor=0, overrideDisplayType=0, overrideColorRGB=None, shapeSetAttrCmd=None):
        self.shapeName = shapeName
        self.lineWidth = lineWidth
        self.overrideEnabled = overrideEnabled
        self.overrideRGBColors = overrideRGBColors
        self.hideOnPlayback = hideOnPlayback
        self.overrideColor = overrideColor
        self.overrideDisplayType = overrideDisplayType
        self.overrideColorRGB = overrideColorRGB if overrideColorRGB is not None else []
        self.shapeSetAttrCmd = shapeSetAttrCmd
        self.get_shapeData(self.shapeName)

    @property
    def attrs(self):
        attr_list = []
        all_node_attr = cmds.listAttr(self.shapeName)
        for attr in ['shapeName', 'lineWidth', 'overrideEnabled', 'overrideRGBColors', 'hideOnPlayback', 'overrideColor', 'overrideDisplayType', 'overrideColorRGB', 'shapeSetAttrCmd']:
            if attr in all_node_attr:
                attr_list.append(attr)
        return attr_list

    def check_shape(self, shape):
        if not cmds.objExists(shape):
            raise RuntimeError("Can not find '{}'".format(shape))
        if cmds.objectType(shape) != "nurbsCurve":
            raise RuntimeError("'{}' is not nurbsCurve".format(shape))

    def get_shapeData(self, shape_object=None):
        self.check_shape(shape_object)

        self.shapeName = shape_object
        for attr in self.attrs:
            if attr == "overrideColorRGB":
                setattr(self, attr, list(cmds.getAttr("{}.{}".format(shape_object, attr))[0]))
            else:
                setattr(self, attr, cmds.getAttr("{}.{}".format(shape_object, attr)))
        self.shapeSetAttrCmd = get_setCvShapeCmd(self.shapeName)

    def set_shapeData(self, shape_object=None, setShape=True, setDrawInfo=True):
        self.check_shape(shape_object)

        if setDrawInfo:
            for attr in self.attrs:
                try:
                    if attr == "overrideColorRGB":
                        cmds.setAttr("{}.{}".format(shape_object, attr), *getattr(self, attr))
                    else:
                        cmds.setAttr("{}.{}".format(shape_object, attr), getattr(self, attr))
                except:
                    cmds.warning("setAttr '{}.{}' fail.".format(shape_object, attr))
        if setShape:
            sel_temp = cmds.ls(sl=1)
            cmds.select(shape_object)
            try:
                mel.eval(self.shapeSetAttrCmd)
            except:
                cmds.warning("setAttr '{}.create' fail.".format(shape_object))
            cmds.select(sel_temp)


class CurveData(yaml.YAMLObject):
    yaml_tag = 'CurveData'

    def __init__(self, transformName="transformName", curveShapeDataList=None):
        self.transformName = transformName
        self.curveShapeDataList = curveShapeDataList if curveShapeDataList is not None else []
        if self.transformName:
            self.curveShapeDataList = []
            self.get_data(self.transformName)
        else:
            raise RuntimeError("please input transform name")

    def get_data(self, transform_obj=None):
        if not transform_obj:
            transform_obj = self.transformName
        if not cmds.objExists(transform_obj):
            raise RuntimeError("Can not find '{}'".format(transform_obj))

        self.transformName = transform_obj
        shape_list = get_cvShapes(self.transformName)
        self.curveShapeDataList = []
        for shape in shape_list:
            self.curveShapeDataList.append(CurveShapeData(shape))

    def set_data(self, transform_obj=None, setShape=True, setDrawInfo=True):
        if not transform_obj:
            transform_obj = self.transformName
        if not cmds.objExists(transform_obj):
            raise RuntimeError("Can not find '{}'".format(transform_obj))

        target_shape_list = get_cvShapes(transform_obj)

        deviation = len(self.curveShapeDataList) - len(target_shape_list)
        if deviation > 0:
            for i in range(deviation):
                if not target_shape_list:
                    shapeName = "{}Shape".format(transform_obj)
                else:
                    shapeName = target_shape_list[-1]
                cmds.createNode("nurbsCurve", p=transform_obj, name=shapeName)

        elif deviation < 0:
            for i in range(abs(deviation)):
                cmds.delete(target_shape_list[-i])
        target_shape_list = get_cvShapes(transform=transform_obj)

        if len(self.curveShapeDataList) == len(target_shape_list):
            for i, x in enumerate(self.curveShapeDataList):
                self.curveShapeDataList[i].set_shapeData(target_shape_list[i], setShape, setDrawInfo)


def getShapes(transform=None, type=None):
    if not transform:
        transform = cmds.ls(sl=1)
    if not type:
        return cmds.listRelatives(transform, ni=True, s=True)
    return cmds.listRelatives(transform, ni=True, s=True, type=type)


def get_cvShapes(transform=None):
    return getShapes(transform, type="nurbsCurve")


def get_setCvShapeCmd(shape_obj):
    mSel = om.MSelectionList()
    mSel.add("{}.local".format(shape_obj))
    mPlug = mSel.getPlug(0)
    cmd_list = mPlug.getSetAttrCmds(useLongNames=True)
    cmd_str = "".join(cmd_list).replace('\t', ' ').replace(".local", ".create")
    return cmd_str


def replace_cvShape(source, target, setShape=True, setDrawInfo=True):
    if type(source) is not str:
        raise RuntimeError("parameter source is not string")
    if type(target) is str:
        target = [target]
    source_shape_list = get_cvShapes(source)
    if not source_shape_list:
        raise RuntimeError("source dont have nurbsCurve shape node")

    cvData = CurveData(source)
    for obj in target:
        cvData.set_data(obj, setShape=setShape, setDrawInfo=setDrawInfo)


def mirror_cvShape(source_list=[], target_list=[], setShape=True, setDrawInfo=False):
    if type(source_list) is str:
        source_list = [source_list]

    for i, obj in enumerate(source_list):
        if not cmds.objExists(obj):
            om.MGlobal.displayInfo("Can not find '{}'.".format(obj))
            continue
        otherSide_obj = target_list[i]
        if not cmds.objExists(otherSide_obj):
            om.MGlobal.displayInfo("Can not find '{}'.".format(otherSide_obj))
            continue
        if obj == otherSide_obj:
            om.MGlobal.displayInfo("'{}' pass.".format(obj))
            continue
        cvData = CurveData(obj)
        cvData.set_data(otherSide_obj, setShape=setShape, setDrawInfo=setDrawInfo)
        obj_shape_list = get_cvShapes(obj)
        otherSide_obj_shape_list = get_cvShapes(otherSide_obj)
        for shape_i, shape in enumerate(obj_shape_list):
            pos_list = cmds.xform("{}.cv[*]".format(shape), q=1, t=1, ws=1)
            pos_ary = [pos_list[i:i+3] for i in range(0, len(pos_list), 3)]
            for cv_i, cv_pos in enumerate(pos_ary):
                cv_pos[0] *= -1
                cmds.xform("{}.cv[{}]".format(otherSide_obj_shape_list[shape_i], cv_i), t=cv_pos, ws=1)


def select_cvControlVertex(curve_list):
    if not curve_list:
        raise RuntimeError("Please input curve.")
    sel_list = []
    for cv in curve_list:
        long_name = "{}.cv[*]".format(cv)
        sel_list += cmds.ls(long_name, fl=1)
    cmds.select(sel_list)


def export_cvData(cv_list=None, path=None, **kwargs):
    if cv_list:
        if type(cv_list) is str:
            cv_list = [cv_list]
    else:
        sel = cmds.ls(sl=1)
        cv_list = []
        for obj in sel:
            if get_cvShapes(obj):
                cv_list.append(obj)

    data_list = []
    for obj in cv_list:
        data_list.append(CurveData(obj))
        
    path = choseFile(path, dialogStyle=2, caption="Export nurbsCurve data", fileFilter="CV YAML file(*.cv)", **kwargs)
    if not path:
        return
    with open(path, "w") as f:
        yaml.dump(data_list, f, indent=4, width=80)
    showMessage("Export shapes successful")


def import_cvData(path=None, **kwargs):
    path = choseFile(path, dialogStyle=2, caption="Import nurbsCurve data", fileFilter="CV YAML file(*.cv)", fileMode=1, **kwargs)
    if not path:
        return
    with open(path, "r") as f:
        data_list = yaml.load(f)
        for data in data_list:
            if cmds.objExists(data.transformName):
                data.set_data()
            else:
                cmds.warning("Can not find '{}'".format(data.transformName))
    showMessage("Import shapes successful")


def mirror_cvShape_cmd():
    sel_list = cmds.ls(sl=1, o=1)
    for i, x in enumerate(sel_list):
        if cmds.objectType(x) == "nurbsCurve":
            sel_list[i] = cmds.listRelatives(x, p=1)[0]
    mirror_cvShape(source_list=sel_list, target_list=MIRROR_CONFIG.exchange(sel_list), setShape=1, setDrawInfo=0)
    msg = "Mirror curve shapes."
    showMessage(MIRROR_CONFIG)
    showMessage(msg)


def replace_cvShape_cmd():
    sel_list = cmds.ls(sl=1, o=1)
    if len(sel_list) < 2:
        raise RuntimeError("Please select at least two objects.")
    for i, x in enumerate(sel_list):
        if cmds.objectType(x) == "nurbsCurve":
            sel_list[i] = cmds.listRelatives(x, p=1)[0]
    replace_cvShape(sel_list[0], sel_list[1:], setShape=1, setDrawInfo=1)
    msg = "Replace curve shapes."
    showMessage(msg)


def select_cvControlVertex_cmd():
    sel_list = cmds.ls(sl=1, o=1)
    select_cvControlVertex(sel_list)
    msg = "Select curve CV."
    showMessage(MIRROR_CONFIG)
    showMessage(msg)


# export_cvData()
# import_cvData()
# replace_cvShape(cmds.ls(sl=1)[0],cmds.ls(sl=1)[1:])
# mirror_cvShape_cmd()
