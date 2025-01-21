import yaml
from dataclasses import dataclass, field

from maya import mel
from maya import cmds
from maya.api import OpenMaya as om
from UTILS.ui.showMessage import showMessage
from UTILS.mirrorEnv import MIRROR_CONFIG


@dataclass
class CurveShapeData(yaml.YAMLObject):
    """ Save nurbsCurveShapeData 

    Data:
        shapeName (str): shape's name
        lineWidth (float): shapes's attr
        overrideEnabled (bool): shapes's attr
        overrideRGBColors (bool): shapes's attr
        hideOnPlayback (bool): shapes's attr
        overrideColor (int): shapes's attr
        overrideDisplayType (int): shapes's attr
        overrideColorRGB (list[float]): shapes's attr
        shapeSetAttrCmd (str): set shape's nurbsCurve data cmd scripts
    """

    yaml_tag = 'CurveShapeData'
    shapeName: str = "shapeName"
    lineWidth: float = 0
    overrideEnabled: bool = False
    overrideRGBColors: bool = False
    hideOnPlayback: bool = False
    overrideColor: int = 0
    overrideDisplayType: int = 0
    overrideColorRGB: list = field(default_factory=list)
    shapeSetAttrCmd: str = None

    def __post_init__(self):
        self.get_shapeData(self.shapeName)

    @property
    def attrs(self):
        attr_list = []
        all_node_attr = cmds.listAttr(self.shapeName)
        for attr in list(self.__dataclass_fields__.keys()):
            if attr in all_node_attr:
                attr_list.append(attr)
        return attr_list

    def check_shape(self, shape):
        """Check shape is exists"""
        if not cmds.objExists(shape):
            raise RuntimeError(f"Can not find '{shape}'")
        if cmds.objectType(shape) != "nurbsCurve":
            raise RuntimeError(f"'{shape}' is not nurbsCurve")

    def get_shapeData(self, shape_object=None):
        """ Get shape data"""
        self.check_shape(shape_object)

        self.shapeName = shape_object
        for attr in self.attrs:
            if attr == "overrideColorRGB":
                setattr(self, attr, list(cmds.getAttr(f"{shape_object}.{attr}")[0]))
            else:
                setattr(self, attr, cmds.getAttr(f"{shape_object}.{attr}"))
        self.shapeSetAttrCmd = get_setCvShapeCmd(self.shapeName)

    def set_shapeData(self, shape_object=None,
                      setShape: bool = True,
                      setDrawInfo: bool = True):
        """Set shape data"""
        self.check_shape(shape_object)

        if setDrawInfo:
            for attr in self.attrs:
                try:
                    if attr == "overrideColorRGB":
                        cmds.setAttr(f"{shape_object}.{attr}", *getattr(self, attr))
                    else:
                        cmds.setAttr(f"{shape_object}.{attr}", getattr(self, attr))
                except:
                    cmds.warning(f"setAttr '{shape_object}.{attr}' fail.")
        if setShape:
            sel_temp = cmds.ls(sl=1)
            cmds.select(shape_object)
            try:
                mel.eval(self.shapeSetAttrCmd)
            except:
                cmds.warning(f"setAttr '{shape_object}.create' fail.")
            cmds.select(sel_temp)


@ dataclass
class CurveData(yaml.YAMLObject):
    """ Save Curve Data
    Args:
        args[0] (str): Curve's transform name
    Data:
        transformName (str):  Curve's transform name
        curveShapeDataList (list[CurveShapeData]):  List of shape's CurveShapeData
    """
    yaml_tag = 'CurveData'
    transformName: str = "transformName"
    curveShapeDataList: list = field(default_factory=list)

    def __post_init__(self):
        if self.transformName:
            self.curveShapeDataList = []
            self.get_data(self.transformName)
        else:
            raise RuntimeError("please input transform name")

    def get_data(self, transform_obj: str = None):
        if not transform_obj:
            transform_obj = self.transformName
        if not cmds.objExists(transform_obj):
            raise RuntimeError(f"Can not find '{transform_obj}'")

        self.transformName = transform_obj
        shape_list = get_cvShapes(self.transformName)
        self.curveShapeDataList.clear()
        for shape in shape_list:
            self.curveShapeDataList.append(CurveShapeData(shape))

    def set_data(self, transform_obj: str = None,
                 setShape: bool = True,
                 setDrawInfo: bool = True):
        if not transform_obj:
            transform_obj = self.transformName
        if not cmds.objExists(transform_obj):
            raise RuntimeError(f"Can not find '{transform_obj}'")

        target_shape_list = get_cvShapes(transform_obj)

        deviation = len(self.curveShapeDataList) - len(target_shape_list)
        if deviation > 0:
            for i in range(deviation):
                if not target_shape_list:
                    shapeName = f"{transform_obj}Shape"
                else:
                    shapeName = target_shape_list[-1]
                cmds.createNode("nurbsCurve", p=transform_obj, name=shapeName)

        elif deviation < 0:
            for i in range(abs(deviation)):
                cmds.delete(target_shape_list[-i])
        target_shape_list = get_cvShapes(transform=transform_obj)

        if len(self.curveShapeDataList) == len(target_shape_list):
            for i, x in enumerate(self.curveShapeDataList):
                self.curveShapeDataList[i].set_shapeData(target_shape_list[i],
                                                         setShape,
                                                         setDrawInfo)


def getShapes(transform=None, type: str = None):
    """Get shapes """
    if not transform:
        transform = cmds.ls(sl=1)
    if not type:
        return cmds.listRelatives(transform, ni=True, s=True)
    return cmds.listRelatives(transform, ni=True, s=True, type=type)


def get_cvShapes(transform=None):
    """get nurbsCurve shapes"""
    return getShapes(transform, type="nurbsCurve")


def get_setCvShapeCmd(shape_obj):
    """get mel about set nurbs curve cmd
    Args:
        shape_obj (str): nurbs curve shape's name

    Returns:
        str: return cmd about set curve shapes
    """
    mSel = om.MSelectionList()
    mSel.add(f"{shape_obj}.local")
    mPlug: om.MPlug = mSel.getPlug(0)
    cmd_list = mPlug.getSetAttrCmds(useLongNames=True)
    cmd_str = "".join(cmd_list).replace('\t', ' ').replace(".local", ".create")
    return cmd_str


def replace_cvShape(source: str,
                    target: list,
                    setShape: bool = True,
                    setDrawInfo: bool = True):
    """ replace curve's shapes
    Args:
        source (str): source curve object
        target (str): target curve object
    """
    if type(source) is not str:
        raise RuntimeError("parameter source is not string")
    if type(target) is str:
        target = [target]
    source_shape_list = get_cvShapes(source)
    if not source_shape_list:
        raise RuntimeError("source dont have nurbsCurve shape node")

    cvData = CurveData(source)
    for obj in target:
        cvData.set_data(obj,
                        setShape=setShape,
                        setDrawInfo=setDrawInfo)


def mirror_cvShape(source_list: list = [],
                   target_list: list = [],
                   setShape: bool = True,
                   setDrawInfo: bool = False):
    """ Mirror the shape of one side to the other side.

    Args:
        object (list, optional): Source transform object list
        replace (list, optional): Replace str[0] with str[1] in the transform object name.
        setShape (bool, optional): If False will be pass mirror shape.
        setDrawInfo (bool, optional): If False will be pass mirror shape draw information.
    """

    if type(source_list) is str:
        source_list = [source_list]

    for i, obj in enumerate(source_list):
        # obj is true
        if not cmds.objExists(obj):
            om.MGlobal.displayInfo(f"Can not find '{obj}'.")
            continue
        # otherSize is true
        otherSide_obj = target_list[i]
        if not cmds.objExists(otherSide_obj):
            om.MGlobal.displayInfo(f"Can not find '{otherSide_obj}'.")
            continue
        # source == target will bee continue
        if obj == otherSide_obj:
            om.MGlobal.displayInfo(f"'{obj}' pass.")
            continue
        # transf cv shape data
        cvData = CurveData(obj)
        cvData.set_data(otherSide_obj, setShape=setShape, setDrawInfo=setDrawInfo)
        # .cv[*] * -1
        obj_shape_list = get_cvShapes(obj)
        otherSide_obj_shape_list = get_cvShapes(otherSide_obj)
        for shape_i, shape in enumerate(obj_shape_list):
            pos_list = cmds.xform(f"{shape}.cv[*]", q=1, t=1, ws=1)
            pos_ary = [pos_list[i:i+3] for i in range(0, len(pos_list), 3)]
            for cv_i, cv_pos in enumerate(pos_ary):
                cv_pos[0] *= -1
                cmds.xform(f"{otherSide_obj_shape_list[shape_i]}.cv[{cv_i}]", t=cv_pos, ws=1)


def select_cvControlVertex(curve_list: list):
    if not curve_list:
        raise RuntimeError("Please input curve.")
    sel_list = []
    for cv in curve_list:
        long_name = f"{cv}.cv[*]"
        sel_list += cmds.ls(long_name, fl=1)
    cmds.select(sel_list)


def export_cvData(cv_list=None):
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

    path = cmds.fileDialog2(dialogStyle=2, caption="Export nurbsCurve data", fileFilter="YAML file(*.yaml)")
    if not path:
        return 
    path = path[0]
    with open(path, "w") as f:
        yaml.dump(data_list, f, sort_keys=False, indent=4, width=80)
    message = '<hl> Export successful </hl>'
    cmds.inViewMessage(amg=message, pos='midCenterBot', fade=True)


def import_cvData():
    path = cmds.fileDialog2(dialogStyle=2, caption="Import nurbsCurve data", fileFilter="YAML file(*.yaml)", fileMode=1)[0]
    if not path:
        return 
    path = path[0]
    with open(path, "r") as f:
        data_list = yaml.unsafe_load(f)
        for data in data_list:
            if cmds.objExists(data.transformName):
                data.set_data()
            else:
                cmds.warning(f"Can not find '{data.transformName}'")
    message = '<hl> Import successful </hl>'
    cmds.inViewMessage(amg=message, pos='midCenterBot', fade=True)


def mirror_cvShape_cmd():
    sel_list = cmds.ls(sl=1, o=1)
    for i, x in enumerate(sel_list):
        if cmds.objectType(x) == "nurbsCurve":
            sel_list[i] = cmds.listRelatives(x, p=1)[0]
    mirror_cvShape(source_list=sel_list,
                   target_list=MIRROR_CONFIG.exchange(sel_list),
                   setShape=1,
                   setDrawInfo=0)
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
