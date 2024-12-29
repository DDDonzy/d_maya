import math
import maya.api.OpenMaya as om
import maya.cmds as cmds


def mirrorTransform(source_object, target_object, mirrorAxis="X"):
    # create mirror matrix
    mirror_matrix = om.MMatrix()
    if mirrorAxis == "X":
        mirror_matrix = om.MMatrix(((-1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
    if mirrorAxis == "Y":
        mirror_matrix = om.MMatrix(((1, 0, 0, 0), (0, -1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
    if mirrorAxis == "Z":
        mirror_matrix = om.MMatrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, -1, 0), (0, 0, 0, 1)))
    # get target parent inverse matrix !!!(parent inverse matrix = parent world inverse matrix)!!!
    targetParentInverse_matrix = om.MMatrix(cmds.getAttr("%s.parentInverseMatrix" % target_object))
    # get source parent matrix   !!!(parent matrix = parent world matrix)!!!
    sourceParent_matrix = om.MMatrix(cmds.getAttr("%s.parentMatrix" % source_object))
    # get source matrix
    source_matrix = om.MMatrix(cmds.getAttr("%s.worldMatrix" % source_object))
    # get offset Matrix after mirror source
    offset_matrix = sourceParent_matrix * mirror_matrix * targetParentInverse_matrix
    # get mirror source matrix
    mirrorSource_matrix = source_matrix * mirror_matrix
    # remap to target and get matrix
    output = offset_matrix * mirrorSource_matrix * targetParentInverse_matrix
    # matrix to transform
    outputTRS = matrix_to_TRS(output, cmds.getAttr("%s.rotateOrder" % source_object))
    # set target transform
    set_TRS(target_object, outputTRS)


def matrix_to_TRS(inputMatrix, rotateOrder=0):
    omMTranMat = om.MTransformationMatrix(inputMatrix)
    T = omMTranMat.translation(1)
    ER = omMTranMat.rotation()
    ER.reorderIt(rotateOrder)
    R = [math.degrees(angle) for angle in [ER.x, ER.y, ER.z]]
    S = omMTranMat.scale(1)
    outputList = [T[0], T[1], T[2],
                  R[0], R[1], R[2],
                  S[0], S[1], S[2], ]
    return outputList


def TRS_to_matrix(TRS, rotateOrder=0):
    omMTranMat = om.MTransformationMatrix()
    T = om.MVector(TRS[0], TRS[1], TRS[2])
    ER = om.MEulerRotation(math.radians(TRS[3]), math.radians(TRS[4]), math.radians(TRS[5]), rotateOrder)
    S = om.MVector(TRS[6], TRS[7], TRS[8])
    omMTranMat.setTranslation(T, 1)
    omMTranMat.setRotation(ER)
    omMTranMat.setScale(S, 1)
    return omMTranMat.asMatrix()


def get_TRS(obj):
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    TRS = []
    for a in attrs:
        TRS.append(cmds.getAttr("%s.%s" % (obj, a)))
    return TRS


def set_TRS(obj, inputTRS):
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    for a in attrs:
        i = attrs.index(a)
        cmds.setAttr("%s.%s" % (obj, a), inputTRS[i])


def createNode_FBF(matrix, name=None):
    matrix = list(matrix)
    matrix_attrs = ["in00", "in01", "in02", "in03",
                    "in10", "in11", "in12", "in13",
                    "in20", "in21", "in22", "in23",
                    "in30", "in31", "in32", "in33"]
    if name:
        FBF = cmds.createNode("fourByFourMatrix", name=name)
    else:
        FBF = cmds.createNode("fourByFourMatrix")

    iterIndex = 0
    for num in matrix:
        attr_name = matrix_attrs[iterIndex]
        cmds.setAttr("%s.%s" % (FBF, attr_name), num)
        iterIndex += 1

    return FBF