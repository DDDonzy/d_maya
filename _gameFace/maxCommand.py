
import textwrap
import face.control as control
from maya import cmds
import yaml
from face.data.config import *


class toMaxCommand():
    def __init__(self):
        self.command = ""

    def __repr__(self):
        return self.command

    def uvPin(self, obj, uvPin, faceIndex, vis):
        vis = bool(vis)
        command = textwrap.dedent("""

        obj = ${0}
        pin = Point()
        pin.name = "{0}_Pin"
        pin.cross = {3}
        pin.centermarker = {3}
        pin.axistripod = {3}
        pin.Box = {3}
        pin.wireColor = color 50 120 20
        pin.isHidden = {3}
        pin.isFrozen = {3}
        pin.parent = obj.parent

        attachController = Attachment()
        pin.pos.controller = attachController
        attachController.node = ${1}
        attachController.align = true
        keyNew = AttachCtrl.addNewKey attachController 0
        keyNew.face = {2}
        keyNew.coord = [0,0]
        AttachCtrl.update attachController

        driver = pin
        driven = obj

        offsetMatrix = driven.transform * inverse driver.transform
        obj_exp = driven.Transform.controller = transform_script ()

        obj_exp.addNode "driver" driver
        obj_exp.addNode "driven" driven
        obj_exp.addConstant "offsetMatrix" offsetMatrix
        obj_exp.script = "offsetMatrix * driver.transform * inverse driven.parent.transform"

        """.format(obj, uvPin, faceIndex, vis))

        self.command += command

    def matrixConstraint(self, driver, driven):

        command = textwrap.dedent("""

        driver = ${0}
        driven = ${1}

        offsetMatrix = driven.transform * inverse driver.transform
        obj_exp = driven.Transform.controller = transform_script ()

        obj_exp.addNode "driver" driver
        obj_exp.addNode "driven" driven
        obj_exp.addConstant "offsetMatrix" offsetMatrix
        obj_exp.script = "offsetMatrix * driver.transform * inverse driven.parent.transform"

        """.format(driver, driven))

        self.command += command

    def limitAll(self, obj):
        command = textwrap.dedent("""

        obj = ${0}

        limit = obj.position.controller.X_Position.controller = float_limit ()
        limit.Enable=True
        limit.upper_limit = 0
        limit.upper_limit_enabled = True
        limit.lower_limit = -0
        limit.lower_limit_enabled = True

        limit = obj.position.controller.Y_Position.controller = float_limit ()
        limit.Enable=True
        limit.upper_limit = 0
        limit.upper_limit_enabled = True
        limit.lower_limit = -0
        limit.lower_limit_enabled = True

        limit = obj.position.controller.Z_Position.controller = float_limit ()
        limit.Enable=True
        limit.upper_limit = 0
        limit.upper_limit_enabled = True
        limit.lower_limit = -0
        limit.lower_limit_enabled = True


        limit = obj.rotation.controller.X_Rotation.controller = float_limit ()
        limit.Enable=True
        limit.upper_limit = 0
        limit.upper_limit_enabled = True
        limit.lower_limit = -0
        limit.lower_limit_enabled = True

        limit = obj.rotation.controller.Y_Rotation.controller = float_limit ()
        limit.Enable=True
        limit.upper_limit = 0
        limit.upper_limit_enabled = True
        limit.lower_limit = -0
        limit.lower_limit_enabled = True

        limit = obj.rotation.controller.Z_Rotation.controller = float_limit ()
        limit.Enable=True
        limit.upper_limit = 0
        limit.upper_limit_enabled = True
        limit.lower_limit = -0
        limit.lower_limit_enabled = True


        limitScale = obj.scale.controller = ScaleXYZ ()
        limit = limitScale.X_Scale.controller = float_limit()
        limit.Enable=True
        limit.upper_limit = 1
        limit.upper_limit_enabled = True
        limit.lower_limit = 1
        limit.lower_limit_enabled = True

        limit = limitScale.Y_Scale.controller = float_limit()
        limit.Enable=True
        limit.upper_limit = 1
        limit.upper_limit_enabled = True
        limit.lower_limit = 1
        limit.lower_limit_enabled = True

        limit = limitScale.Z_Scale.controller = float_limit()
        limit.Enable=True
        limit.upper_limit = 1
        limit.upper_limit_enabled = True
        limit.lower_limit = 1
        limit.lower_limit_enabled = True

        """.format(obj))

        self.command += command

    def unLimit(self, obj, axis, limit):

        command = textwrap.dedent("""
        limit = ${0}.position.controller.{1}_Position.controller = linear_float()
        limit = ${0}.position.controller.{1}_Position.controller = float_limit()
        limit.Enable=True
        limit.upper_limit = {2}
        limit.upper_limit_enabled = True
        limit.lower_limit = {3}
        limit.lower_limit_enabled = True

        """.format(obj, axis, max(*limit), min(*limit)))
        self.command += command

    def sdk(self, driver, mesh, driverValue, drivenValue, axis, index):
        command = textwrap.dedent("""

        b1 = ${0}.controller.position.controller.{1}_Position.controller
        bs = ${2}.morpher

        dv_min = {4}
        dv_max = {5}

        v1 = {6}
        v2 = {7}

        cont = bs[{3}].controller = Float_Reactor()
        reactTo cont b1

        createReaction cont


        setReactionValue cont 1 dv_min
        setReactionValue cont 2 dv_max


        setReactionState cont 1 v1
        setReactionState cont 2 v2



        """.format(driver,
                   axis.upper(),
                   mesh,
                   index,
                   min(driverValue),
                   max(driverValue),
                   drivenValue[driverValue.index(min(driverValue))],
                   drivenValue[driverValue.index(max(driverValue))]))
        self.command += command


command = toMaxCommand()

# joint constraint
all_sk = control.get_allSkinJoint()
for sk in all_sk:
    ctl = control.ControlData(sk)
    command.matrixConstraint(driver=ctl.loc, driven=sk)

# uvpin -> attachment
uvPinList = ['Head_uvPinMesh', "Jaw_uvPinMesh", "part_uvPinMesh", "Sec_uvPinMesh"]
for uvPin in uvPinList:
    data = yaml.load(cmds.getAttr("{}.notes".format(uvPin)))
    for x in data:
        command.uvPin(obj=x["driven"], uvPin=uvPin, faceIndex=(x["meshComponent"][0]/5)*4, vis=False)

# sdk
data = yaml.load(cmds.getAttr("FaceBridge.notes"))
for i, x in enumerate(data):
    if x.driverAttr:
        axis = x.driverAttr[-1]
        driverValue = [x.min, x.max]
        index = i+1
        driver = x.driverAttr.split(".")[0]

        for mesh in ['Head_uvPinMesh', "Jaw_uvPinMesh", "part_uvPinMesh", "Sec_uvPinMesh"]:
            command.sdk(driver=driver, mesh=mesh, driverValue=driverValue, drivenValue=[0, 100], axis=axis, index=index)

# limit
ctl = []
data = {}
data = yaml.load(cmds.getAttr("FaceBridge.notes"))
for i, x in enumerate(data):
    if x.driverAttr:
        driver = x.driverAttr.split(".")[0]
        if driver not in ctl:
            ctl.append(driver)
for x in ctl:
    command.limitAll(x)
    v = eval("cmds.transformLimits('{}',q=1,tx=1)".format(x))
    command.unLimit(x, "x", v)
    v = eval("cmds.transformLimits('{}',q=1,ty=1)".format(x))
    command.unLimit(x, "y", v)