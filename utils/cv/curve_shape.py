import yaml
from dataclasses import dataclass, field

from maya import mel
from maya import cmds
from maya.api import OpenMaya as om


@dataclass
class CurveShapeData(yaml.YAMLObject):
    yaml_tag = 'CurveShapeData'
    shapeName: str = "shapeName"
    lineWidth: int = 0
    overrideEnabled: bool = False
    overrideRGBColors: bool = False
    hideOnPlayback: bool = False
    overrideColor: int = 0
    overrideDisplayType: int = 0
    overrideColorRGB: list = field(default_factory=list)
    shapeSetAttrCmd: str = None

    def __post_init__(self):
        self.get_from_shape(self.shapeName)

    @property
    def attrs(self):
        attr_list = []
        all_node_attr = cmds.listAttr(self.shapeName)
        for attr in list(self.__dataclass_fields__.keys()):
            if attr in all_node_attr:
                attr_list.append(attr)
        return attr_list

    def check_shape(self, shape):
        if not cmds.objExists(shape):
            raise RuntimeError(f"Can not find '{shape}'")
        if cmds.objectType(shape) != "nurbsCurve":
            raise RuntimeError(f"'{shape}' is not nurbsCurve")

    def get_from_shape(self, shape_object=None):
        self.check_shape(shape_object)

        self.shapeName = shape_object
        for attr in self.attrs:
            if attr == "overrideColorRGB":
                setattr(self, attr, list(cmds.getAttr(f"{shape_object}.{attr}")[0]))
            else:
                setattr(self, attr, cmds.getAttr(f"{shape_object}.{attr}"))
        self.shapeSetAttrCmd = get_nurbsCurveType_setAttrCmd(self.shapeName)

    def set_to_shape(self, shape_object=None,
                     setShape: bool = True,
                     setDrawInfo: bool = True):
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
    yaml_tag = 'CurveData'
    transformName: str = "transformName"
    shapes: list = field(default_factory=list)

    def __post_init__(self):
        if self.transformName:
            self.shapes = []
            self.get_data(self.transformName)
        else:
            raise RuntimeError("please input transform name")

    def get_data(self, transform_obj: str = None):
        if not transform_obj:
            transform_obj = self.transformName
        if not cmds.objExists(transform_obj):
            raise RuntimeError(f"Can not find '{transform_obj}'")

        self.transformName = transform_obj
        shape_list = get_curve_shape(self.transformName)
        self.shapes.clear()
        for shape in shape_list:
            self.shapes.append(CurveShapeData(shape))

    def set_data(self, transform_obj: str = None,
                 setShape: bool = True,
                 setDrawInfo: bool = True):
        if not transform_obj:
            transform_obj = self.transformName
        if not cmds.objExists(transform_obj):
            raise RuntimeError(f"Can not find '{transform_obj}'")

        target_shape_list = get_curve_shape(transform_obj)

        deviation = len(self.shapes) - len(target_shape_list)
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
        target_shape_list = get_curve_shape(transform_object=transform_obj)

        if len(self.shapes) == len(target_shape_list):
            for i, x in enumerate(self.shapes):
                self.shapes[i].set_to_shape(target_shape_list[i],
                                            setShape,
                                            setDrawInfo)


def get_curve_shape(transform_object):
    """get nurbsCurve shapes
    Args:
        transform_object (str): transform name

    Returns:
        list: return shape list
    """
    if not cmds.objExists(transform_object):
        raise RuntimeError(transform_object + "is not exists")
    shape_list = []
    mSel = om.MSelectionList()
    mSel.add(transform_object)
    mDag = mSel.getDagPath(0)
    num_shape = mDag.numberOfShapesDirectlyBelow()
    for i in range(num_shape):
        mDag = mSel.getDagPath(0)
        mDag.extendToShape(i)
        if mDag.node().apiTypeStr == "kNurbsCurve":
            shape_list.append(mDag.partialPathName())
    return shape_list


def get_nurbsCurveType_setAttrCmd(shape_obj):
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


def replace_curve_shape(source, target,
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
    source_shape_list = get_curve_shape(source)
    if not source_shape_list:
        raise RuntimeError("source dont have nurbsCurve shape node")

    cvData = CurveData(source)
    for obj in target:
        cvData.set_data(obj,
                        setShape=setShape,
                        setDrawInfo=setDrawInfo)


def name_replace(name: str,
                 replace: list = ["L_", "R_"]):
    """input a name and replace str

    Args:
        name (str): _description_
        replace (list, optional): _description_. Defaults to ["L_", "R_"].
    Returns:
        str: replaced name
    """
    if replace[0] in name:
        name = name.replace(*replace)
    elif replace[1] in name:
        replace.reverse()
        name = name.replace(*replace)
    else:
        raise RuntimeError(f"object '{name}' replace error,'{replace[0]}' or '{replace[1]}' not in it.")
    return name


def mirror_curve_shape(object: list = [],
                       replace: list = ["L_", "R_"],
                       setShape: bool = True,
                       setDrawInfo: bool = False):
    """ Mirror the shape of one side to the other side.

    Args:
        object (list, optional): Source transform object list
        replace (list, optional): Replace str[0] with str[1] in the transform object name.
        setShape (bool, optional): If False will be pass mirror shape.
        setDrawInfo (bool, optional): If False will be pass mirror shape draw information.
    """

    if type(object) is str:
        object = [object]

    for obj in object:
        # obj is true
        if not cmds.objExists(obj):
            om.MGlobal.displayInfo(f"Can not find '{obj}'.")
            continue
        # otherSize is true
        try:
            otherSide_obj = name_replace(obj, replace)
        except RuntimeError:
            om.MGlobal.displayInfo(f"Can not find '{otherSide_obj}'.")
            continue
        # transf cv shape data
        cvData = CurveData(obj)
        cvData.set_data(otherSide_obj, setShape=setShape, setDrawInfo=setDrawInfo)
        # .cv[*] * -1
        obj_shape_list = get_curve_shape(obj)
        otherSide_obj_shape_list = get_curve_shape(otherSide_obj)
        for shape_i, shape in enumerate(obj_shape_list):
            pos_list = cmds.xform(f"{shape}.cv[*]", q=1, t=1, ws=1)
            pos_ary = [pos_list[i:i+3] for i in range(0, len(pos_list), 3)]
            for cv_i, cv_pos in enumerate(pos_ary):
                cv_pos[0] *= -1
                cmds.xform(f"{otherSide_obj_shape_list[shape_i]}.cv[{cv_i}]", t=cv_pos, ws=1)


def export_curve_data(cv_list=None):
    if cv_list:
        if type(cv_list) is str:
            cv_list = [cv_list]
    else:
        sel = cmds.ls(sl=1)
        cv_list = []
        for obj in sel:
            if get_curve_shape(obj):
                cv_list.append(obj)

    data_list = []
    for obj in cv_list:
        data_list.append(CurveData(obj))

    path = cmds.fileDialog2(dialogStyle=2, caption="Export nurbsCurve data", fileFilter="YAML file(*.yaml)")[0]
    with open(path, "w") as f:
        yaml.dump(data_list, f, sort_keys=False, indent=4, width=80)
    message = '<hl> Export successful </hl>'
    cmds.inViewMessage(amg=message, pos='midCenterBot', fade=True)


def import_curve_data():
    path = cmds.fileDialog2(dialogStyle=2, caption="Import nurbsCurve data", fileFilter="YAML file(*.yaml)", fileMode=1)[0]
    with open(path, "r") as f:
        data_list = yaml.unsafe_load(f)
        for data in data_list:
            if cmds.objExists(data.transformName):
                data.set_data()
            else:
                cmds.warning(f"Can not find '{data.transformName}'")
    message = '<hl> Import successful </hl>'
    cmds.inViewMessage(amg=message, pos='midCenterBot', fade=True)


# export_curve_data()
# import_curve_data()
# replace_curve_shape(cmds.ls(sl=1)[0],cmds.ls(sl=1)[1:])
# mirror_curve_shape(cmds.ls(sl=1), setShape=1, setDrawInfo=0)
