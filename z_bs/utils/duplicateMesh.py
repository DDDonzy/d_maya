from maya import cmds
from maya.api import OpenMaya as om
from z_bs.utils import apiundo


class DuplicateMeshCommand:
    def __init__(self, source, name):
        self.source = source
        self.name = name
        self.actual_created_name = None

    def doit(self):
        mSel = om.MSelectionList()
        mSel.add(self.source)
        source_shape_mDag = mSel.getDagPath(0)
        source_transform_mDag = om.MDagPath(source_shape_mDag)
        source_transform_fn = om.MFnTransform(source_transform_mDag)
        source_matrix = source_transform_fn.transformation().asMatrix()
        source_fnMesh = om.MFnMesh(source_shape_mDag)
        new_shape_mObj = source_fnMesh.copy(source_fnMesh.object())
        new_transform_fn = om.MFnTransform(new_shape_mObj)
        new_transform_fn.setTransformation(om.MTransformationMatrix(source_matrix))
        self.actual_created_name = new_transform_fn
        return new_transform_fn.setName(self.name)

    def undo(self):
        dag_modifier = om.MDagModifier()
        dag_modifier.deleteNode(self.actual_created_name.object())
        dag_modifier.doIt()

    def execute(self):
        name = self.doit()
        apiundo.commit(self.undo, self.doit)
        return name


def duplicate_mesh(source: str = None, name: str = None) -> str:
    if not source:
        source = cmds.ls(sl=1)[0]
    if not name:
        name = f"{source}_duplicate"
    command = DuplicateMeshCommand(source=source, name=name)
    return command.execute()


if __name__ == "__main__":
    duplicate_mesh()
