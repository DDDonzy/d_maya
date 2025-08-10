from maya.api import OpenMaya as om

weightsDict = {}

mRichSel = om.MGlobal.getRichSelection()
sel = mRichSel.getSelection()

_, comp = sel.getComponent(0)

fnComp = om.MFnSingleIndexedComponent(comp)
if fnComp.hasWeights is False:
    raise RuntimeError("Component has no weights, Please use soft selection.")

for i in range(fnComp.elementCount):
    weightsDict[fnComp.element(i)] = fnComp.weight(i).influence


tup = sorted(weightsDict.items(), key=lambda x: x[1], reverse=True)
print(tup)
print(fnComp.elementCount)

