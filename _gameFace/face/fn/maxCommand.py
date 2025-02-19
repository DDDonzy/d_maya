
import textwrap
import face.fit as fit
import face.control as control
from maya import cmds
import yaml


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
        
        attachController = Attachment()
        pin.pos.controller = attachController
        attachController.node = ${1}
        attachController.align = true
        keyNew = AttachCtrl.addNewKey attachController 0
        keyNew.face = {2}
        keyNew.coord = [0,0]
        
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


command = toMaxCommand()


all_sk = control.get_allSkinJoint()
for sk in all_sk:
    ctl = control.ControlData(sk)
    command.matrixConstraint(driver=ctl.loc, driven=sk)

uvPinList = ['Head_uvPinMesh', "Jaw_uvPinMesh", "part_uvPinMesh", "Sec_uvPinMesh"]
for uvPin in uvPinList:
    data = yaml.load(cmds.getAttr("{}.notes".format(uvPin)))
    for x in data:
        command.uvPin(obj=x["driven"], uvPin=uvPin, faceIndex=x["meshComponent"][1], vis=False)