import textwrap
import face.control as control
from maya import cmds, mel
import yaml
from face.data.config import *
from face.fn.choseFile import choseFile


class toMaxCommand():
    def __init__(self):
        self._command = ""

    def __repr__(self):
        return self._command

    @property
    def command(self):
        self._importFbx = ""
        self._command = ""
        # import fbx
        self.maxImportFbx()

        # mute scene
        self.disableSceneRedraw()
        self.deleteKeys()

        # joint constraint
        all_sk = control.get_allSkinJoint()
        un_sk = cmds.listRelatives(UN_SKIN_JOINT_ROOT, c=1)
        for sk in un_sk:
            if cmds.objectType(sk, isa="joint"):
                all_sk.append(sk)
        for sk in all_sk:
            ctl = control.ControlData(sk)
            self.matrixConstraint(driver=ctl.loc, driven=sk)
        # uvpin -> attachment
        uvPinList = ['Head_uvPinMesh', "Jaw_uvPinMesh", "part_uvPinMesh", "Sec_uvPinMesh"]
        for uvPin in uvPinList:
            data = yaml.load(cmds.getAttr("{}.notes".format(uvPin)))
            for x in data:
                self.uvPin(obj=x["driven"], uvPin=uvPin, faceIndex=(x["meshComponent"][0]/5)*4, vis=False)
        # sdk
        data = yaml.load(cmds.getAttr("FaceBridge.notes"))
        for i, x in enumerate(data):
            if x.driverAttr:
                axis = x.driverAttr[-1]
                driverValue = [x.min, x.max]
                index = i+1
                driver = x.driverAttr.split(".")[0]
                for mesh in ['Head_uvPinMesh', "Jaw_uvPinMesh", "part_uvPinMesh", "Sec_uvPinMesh"]:
                    self.sdk(driver=driver, mesh=mesh, driverValue=driverValue, drivenValue=[0, 100], axis=axis, index=index)
        # class matrix constraint
        sec_list = control.get_controlsByLabel(SEC_LABEL)
        sec_loc = [x.loc for x in sec_list]
        class_list = control.get_controlsByLabel(CLASS_LABEL)
        for x in class_list:
            children = cmds.listRelatives(x.ctl, c=1)
            for c in children:
                if cmds.objectType(c) != "transform":
                    continue
                ctl = control.ControlData(c)
                if ctl.loc in sec_loc:
                    continue
                if ctl.loc != x.loc:
                    self.classMatrixConstraint(driver=x.loc, driver_grp=x.grp, driven=ctl.sdk, driven_grp=ctl.grp)
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
            self.limitAll(x)
            v = eval("cmds.transformLimits('{}',q=1,tx=1)".format(x))
            self.unLimit(x, "x", v)
            v = eval("cmds.transformLimits('{}',q=1,ty=1)".format(x))
            self.unLimit(x, "y", v)
        # freeze hide
        self.hiddenChildren("RigAsset")
        self.hiddenChildren("SkinJoint_GRP")
        self.hiddenChildren("UnSkinJoint_GRP")

        self.freezeChildren("Face_Main")
        self.freezeChildren("RigAsset")
        self.freezeChildren("SkinJoint_GRP")
        self.freezeChildren("UnSkinJoint_GRP")
        # color
        cv = {}
        for x in cmds.ls(type="nurbsCurve"):
            parent = cmds.listRelatives(x, p=1)[0]
            if cmds.getAttr(x+".overrideRGBColors"):
                rgb = cmds.getAttr(x+".overrideColorRGB")[0]
            else:
                rgb = toMaxCommand.canvas_color(cmds.getAttr(x+".overrideColor"))
            rgb = (rgb[0]*255, rgb[1]*255, rgb[2]*255)
            cv.update({parent: rgb})
        for k, v in cv.items():
            self.setColor(k, v)
        # un mute scene
        self.enableSceneRedraw()
        # combine command
        self._command = self._importFbx.replace("##FACE_RIG_LOGIC##", self._command)

        return self._command

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

        self._command += command

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

        self._command += command

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

        self._command += command

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
        self._command += command

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
        self._command += command

    def classMatrixConstraint(self, driver, driver_grp, driven, driven_grp):

        command = textwrap.dedent("""

        class_grp = ${0}
        class_loc = ${1}
        ctl_grp = ${2}
        ctl_sdk = ${3}

        obj_exp = ctl_sdk.Transform.controller = transform_script ()

        obj_exp.addNode "class_grp" class_grp
        obj_exp.addNode "class_loc" class_loc
        obj_exp.addNode "ctl_grp" ctl_grp

        obj_exp.script = "ctl_grp.transform * inverse class_grp.transform * class_loc.transform * inverse ctl_grp.transform"

        """.format(driver_grp, driver, driven_grp, driven))

        self._command += command

    def disableSceneRedraw(self):
        command = textwrap.dedent("""
        disableSceneRedraw()
        """)
        self._command += command

    def enableSceneRedraw(self):
        command = textwrap.dedent("""
        enableSceneRedraw()
        """)
        self._command += command

    def deleteKeys(self):
        command = textwrap.dedent("""
                                  for obj in objects do (if isValidNode obj do (deleteKeys obj))
                                  """)
        self._command += command

    def freezeChildren(self, groupName):
        command = textwrap.dedent("""
                                  objList = ${0}*...*

                                  for x in objList do
                                  (
                                    x.isFrozen  = true
                                  )
                                  """).format(groupName)
        self._command += command

    def hiddenChildren(self, groupName):
        command = textwrap.dedent("""
                                  objList = ${0}*...*

                                  for x in objList do
                                  (
                                    x.isHidden  = true
                                  )
                                  """).format(groupName)
        self._command += command

    def setColor(self, obj, colorRGB):
        command = textwrap.dedent("""
                                  obj = ${0}
                                  obj.wireColor = color {1} {2} {3}
                                  """).format(obj, colorRGB[0], colorRGB[1], colorRGB[2])
        self._command += command

    @staticmethod
    def mayaExportFaceFBX(path=None):

        cmds.loadPlugin('fbxmaya', qt=True)

        cmds.select([RIG_ASSET, CONTROL_ROOT, SKIN_JOINT_ROOT, UN_SKIN_JOINT_ROOT, GEOMETRY_ROOT])

        path = choseFile(path=path, dialogStyle=2, caption="Export FBX", fileFilter="FBX file(*.fbx)")
        if path is None:
            return
        mel.eval('FBXResetExport')
        mel.eval('FBXExportInputConnections -v 0')
        mel.eval('FBXExportIncludeChildren -v 1')
        mel.eval('FBXExportBakeComplexAnimation -v 0')
        mel.eval('FBXExportShapes -v 1')
        mel.eval('FBXExportSkins -v 1')

        mel.eval('FBXExport -f "{}" -s'.format(path))

    def maxImportFbx(self):
        command = textwrap.dedent("""
                                  
        fn getFilePath = (
        filePath = getOpenFileName \
            caption:"Import FBX File" \
            types:"FBX File (*.fbx)|*.fbx|All File (*.*)|*.*" \
            historyCategory:"FBXImports"

        if filePath != undefined then (
            return filePath
        ) else (
            return undefined
        )
        )

        fbxFilePath = getFilePath()
        if not doesFileExist fbxFilePath then (
            messageBox ("Can not find:" + fbxFilePath)
            return false
            )
        else(
            max file new
            FBXImporterSetParam "Animation" false        
            FBXImporterSetParam "Cameras" false        
            FBXImporterSetParam "Lights" false         
            FBXImporterSetParam "Skin" true            
            FBXImporterSetParam "Shape" true           
            FBXImporterSetParam "ImportBoneAsDummy" false
            FBXImporterSetParam "Mode" #merge
            importFile fbxFilePath #noPrompt using:FBXIMP
            forceCompleteRedraw()
            ##FACE_RIG_LOGIC##
            )
                                  """)
        self._importFbx += command

    def exportMaxScript(self, path=None):
        path = choseFile(path=path, dialogStyle=2, caption="Export Max Script", fileFilter="Max Script file(*.ms)")
        if path is None:
            return
        with open(path, "w") as f:
            f.write(self.command)
        print("Export successful")

    def exportToMax(self):
        path = choseFile(dialogStyle=2, caption="Export Max Script", fileFilter="Max Script file(*.ms)")
        if path is None:
            return
        fbx_path = path.replace(".ms", ".fbx")
        self.exportMaxScript(path)
        self.mayaExportFaceFBX(fbx_path)

    @staticmethod
    def canvas_color(index):
        if index == 0:
            return (0.627, 0.627, 0.627)

        elif index == 1:
            return (0, 0, 0)

        elif index == 2:
            return (0.247, 0.247, 0.247)

        elif index == 3:
            return (0.498, 0.498, 0.498)

        elif index == 4:
            return (0.608, 0, 0.157)

        elif index == 5:
            return (0, 0.016, 0.373)

        elif index == 6:
            return (0, 0, 1)

        elif index == 7:
            return (0, 0.275, 0.094)

        elif index == 8:
            return (0.145, 0, 0.263)

        elif index == 9:
            return (0.78, 0, 0.78)

        elif index == 10:
            return (0.537, 0.278, 0.2)

        elif index == 11:
            return (0.243, 0.133, 0.122)

        elif index == 12:
            return (0.6, 0.145, 0)

        elif index == 13:
            return (1, 0, 0)

        elif index == 14:
            return (0, 1, 0)

        elif index == 15:
            return (0, 0.255, 0.6)

        elif index == 16:
            return (1, 1, 1)

        elif index == 17:
            return (1, 1, 0)

        elif index == 18:
            return (0.388, 0.863, 1)

        elif index == 19:
            return (0.263, 1, 0.635)

        elif index == 20:
            return (1, 0.686, 0.686)

        elif index == 21:
            return (0.89, 0.675, 0.475)

        elif index == 22:
            return (1, 1, 0.384)

        elif index == 23:
            return (0, 0.6, 0.325)

        elif index == 24:
            return (0.627, 0.412, 0.188)

        elif index == 25:
            return (0.62, 0.627, 0.188)

        elif index == 26:
            return (0.408, 0.627, 0.188)

        elif index == 27:
            return (0.188, 0.627, 0.365)

        elif index == 28:
            return (0.188, 0.627, 0.627)

        elif index == 29:
            return (0.188, 0.404, 0.627)

        elif index == 30:
            return (0.435, 0.188, 0.627)

        else:
            return (0.627, 0.188, 0.412)


if __name__ == "__main__":
    maxCommand = toMaxCommand()
    maxCommand.exportToMax()
