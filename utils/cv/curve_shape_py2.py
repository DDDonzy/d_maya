import yaml
import maya.cmds as cmds
import maya.mel as mel
from maya.api import OpenMaya as om


class CurveShapeData(yaml.YAMLObject):
    yaml_tag = 'CurveShapeData'

    def __init__(self, shapeName="shapeName"):
        self.shapeName = shapeName
        self.lineWidth = 0
        self.overrideEnabled = False
        self.overrideRGBColors = False
        self.hideOnPlayback = False
        self.overrideColor = 0
        self.overrideDisplayType = 0
        self.overrideColorRGB = []
        self.shapeSetAttrCmd = None
        self.get_from_shape(self.shapeName)

    def __post_init__(self):
        self.get_from_shape(self.shapeName)

    @property
    def attrs(self):
        attr_list = []
        all_node_attr = cmds.listAttr(self.shapeName)
        for attr in self.__dict__.keys():
            if attr in all_node_attr:
                attr_list.append(attr)
        return attr_list

    def check_shape(self, shape):
        if not cmds.objExists(shape):
            raise RuntimeError("Can not find '{0}'".format(shape))
        if cmds.objectType(shape) != "nurbsCurve":
            raise RuntimeError("'{0}' is not nurbsCurve".format(shape))

    def get_from_shape(self, shape_object=None):
        self.check_shape(shape_object)
        self.shapeName = shape_object
        for attr in self.attrs:
            if attr == "overrideColorRGB":
                setattr(self, attr, list(cmds.getAttr("{0}.{1}".format(shape_object, attr))[0]))
            else:
                setattr(self, attr, cmds.getAttr("{0}.{1}".format(shape_object, attr)))
        self.shapeSetAttrCmd = get_nurbsCurveType_setAttrCmd(self.shapeName)

    def set_to_shape(self, shape_object=None):
        self.check_shape(shape_object)
        for attr in self.attrs:
            try:
                if attr == "overrideColorRGB":
                    cmds.setAttr("{0}.{1}".format(shape_object, attr), *getattr(self, attr))
                else:
                    cmds.setAttr("{0}.{1}".format(shape_object, attr), getattr(self, attr))
            except:
                cmds.warning("setAttr '{0}.{1}' fail".format(shape_object, attr))
        sel_temp = cmds.ls(sl=1)
        cmds.select(shape_object)
        try:
            mel.eval(self.shapeSetAttrCmd)
        except:
            cmds.warning("setAttr '{}.create' fail".format(shape_object))
        cmds.select(sel_temp)


class CurveData(yaml.YAMLObject):
    yaml_tag = 'CurveData'

    def __init__(self, transformName="transformName"):
        self.transformName = transformName
        self.shapes = []
        if self.transformName:
            self.get_data(self.transformName)
        else:
            raise RuntimeError("please input transform name")

    def get_data(self, transform_obj=None):
        if not transform_obj:
            transform_obj = self.transformName
        if not cmds.objExists(transform_obj):
            raise RuntimeError("Can not find '{0}'".format(transform_obj))

        self.transformName = transform_obj
        shape_list = get_curve_shape(self.transformName)
        self.shapes = []
        for shape in shape_list:
            self.shapes.append(CurveShapeData(shape))

    def set_data(self, transform_obj=None):
        if not transform_obj:
            transform_obj = self.transformName
        if not cmds.objExists(transform_obj):
            raise RuntimeError("Can not find '{0}'".format(transform_obj))

        target_shape_list = get_curve_shape(transform_obj)

        deviation = len(self.shapes) - len(target_shape_list)
        if deviation > 0:
            for i in range(deviation):
                if not target_shape_list:
                    shapeName = "{0}Shape".format(transform_obj)
                else:
                    shapeName = target_shape_list[-1]
                cmds.createNode("nurbsCurve", p=transform_obj, name=shapeName)

        elif deviation < 0:
            for i in range(abs(deviation)):
                cmds.delete(target_shape_list[-i])

        target_shape_list = get_curve_shape(transform_obj)

        if len(self.shapes) == len(target_shape_list):
            for i, x in enumerate(self.shapes):
                self.shapes[i].set_to_shape(target_shape_list[i])


def get_curve_shape(transform_object):
    """get nurbsCurve shapes 
    Args:
        transform_object (str): transform name

    Returns:
        list: return shape list 
    """
    if not cmds.objExists(transform_object):
        raise RuntimeError(transform_object + " is not exists")
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
    mSel.add("{}.local".format(shape_obj))
    mPlug = mSel.getPlug(0)
    cmd_list = mPlug.getSetAttrCmds(useLongNames=True)
    cmd_str = "".join(cmd_list).replace('\t', ' ').replace(".local", ".create")
    return cmd_str


def replace_curve_shape(source, target):
    """ replace curve's shapes
    Args:
        source (str): source curve transform
        target (str): target curve transform
    """
    if not isinstance(source, (str, unicode)):
        raise RuntimeError("parameter source is not string")
    if isinstance(target, (str, unicode)):
        target = [target]
    source_shape_list = get_curve_shape(source)
    if not source_shape_list:
        raise RuntimeError("source doesn't have nurbsCurve shape node")

    cvData = CurveData(source)
    for obj in target:
        cvData.set_data(obj)


def export_curve_data(cv_list=None):
    if cv_list:
        if isinstance(cv_list, (str, unicode)):
            cv_list = [cv_list]
    else:
        sel = cmds.ls(sl=True)
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


def import_curve_data(cv_list=None):
    path = cmds.fileDialog2(dialogStyle=2, caption="Import nurbsCurve data", fileFilter="YAML file(*.yaml)", fileMode=1)[0]
    with open(path, "r") as f:
        data_list = yaml.unsafe_load(f)
        for data in data_list:
            if cmds.objExists(data.transformName):
                data.set_data()
            else:
                cmds.warning("Can not find '{}'".format(data.transformName))
    message = '<hl> Import successful </hl>'
    cmds.inViewMessage(amg=message, pos='midCenterBot', fade=True)


# export_curve_data()
# import_curve_data()
# replace_curve_shape(cmds.ls(sl=1)[0],cmds.ls(sl=1)[1:])
