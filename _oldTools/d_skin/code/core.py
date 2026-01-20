import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import marshal
class D_skinTool (oma.MFnSkinCluster):

    def __init__(self, skinNodeName):
        self.skinNodeName = skinNodeName
        self.load(self.skinNodeName)

    def load(self, skinNodeName):
        skinNodeMObject = self.toApiMObject(skinNodeName)
        oma.MFnSkinCluster.__init__(self, skinNodeMObject)

    def toApiMObject(self, name):
        MSelection = om.MSelectionList().add(name)
        MObject = MSelection.getDependNode(0)
        return MObject

    def toApiMDagPath(self, name):
        MSelection = om.MSelectionList().add(name)
        MDagPath = MSelection.getDagPath(0)
        return MDagPath

    def getNameByDagPath(self, dagPath):
        MSelection = om.MSelectionList().add(dagPath)
        stringName = om.MFnDependencyNode(MSelection.getDependNode(0)).name()
        return stringName

    def getShape(self):
        shape = cmds.skinCluster(self.skinNodeName, q=True, g=True)
        return shape

    def getSkinWeights(self, *infIndex):
        meshMObject = self.toApiMDagPath(self.getShape()[0])
        singleIdComp = om.MFnSingleIndexedComponent()
        vertexComp = singleIdComp.create(om.MFn.kMeshVertComponent)

        weightData = self.getWeights(meshMObject, vertexComp, *infIndex)
        return weightData

    def getInfluenceIndex(self, influenceName):
        influenceIndex = cmds.skinCluster(self.skinNodeName, q=1, inf=1).index(influenceName)
        return influenceIndex

    def setInfluenceWeights(self, influenceIndex, weights):
        meshMObject = self.toApiMDagPath(self.getShape()[0])

        singleIdComp = om.MFnSingleIndexedComponent()
        vertexComp = singleIdComp.create(om.MFn.kMeshVertComponent)

        if type(influenceIndex) == int:
            influenceIndexArray = om.MIntArray().append(influenceIndex)
        if type(influenceIndex) == list:
            influenceIndexArray = om.MIntArray(influenceIndex)
        if type(weights) == list:
            weights = om.MDoubleArray(weights)

        self.setWeights(meshMObject, vertexComp, influenceIndexArray, weights, normalize=True, returnOldWeights=False)

    def exportWeights(self):
        weightsInfo = self.getSkinWeights()
        influenceNameList = self.influenceObjects()
        influenceNameList = [self.getNameByDagPath(x) for x in influenceNameList]
        weights = weightsInfo[0]
        influenceNum = weightsInfo[-1]
        influenceIndexDict = {}
        for x in influenceNameList:
            influenceIndexDict.update({self.getInfluenceIndex(x): x})          
        return [influenceIndexDict, weights]
    def importWeights(self , weightsInfo):
        base_influenceIndexDict = weightsInfo[0]
        weights = weightsInfo[1]
        influenceIndexArray = om.MIntArray()
        meshMObject = self.toApiMDagPath(self.getShape()[0])
        singleIdComp = om.MFnSingleIndexedComponent()
        vertexComp = singleIdComp.create(om.MFn.kMeshVertComponent)
        def_InfluenceIndexDict = self.exportWeights()[0]
        for bk,bv in base_influenceIndexDict.items():
            for dk,dv in def_InfluenceIndexDict.items():
                if dv == bv:
                    influenceIndexArray.append(dk)
        self.setWeights(meshMObject, vertexComp, influenceIndexArray, weights, normalize=True, returnOldWeights=False)
def exportWeights_file(self):
    sel_list = cmds.ls(sl=1)
    for x in sel_list:
        his = cmds.listHistory(x)
        for n in his:
            if cmds.objectType(n)=="skinCluster":
                return n
        sk_node = D_skinTool(n)
        weightsInfo = sk_node.exportWeights()
        path = cmds.fileDialog2(dialogStyle=2, caption="Export skin weights", fileFilter="Weights Files (*.w)")[0]

        exportFile = open(path, 'wb')
        marshal.dump(weightsInfo, exportFile)
        exportFile.close()
        cmds.progressWindow(endProgress=1)
        om.MPxCommand().displayInfo('Export Successful')
