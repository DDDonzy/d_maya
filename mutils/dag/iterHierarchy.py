from maya.api import OpenMaya as om
from typing import Tuple, Union


class IterHierarchy:
    def __init__(self, root: Union[str, om.MDagPath], skipShape=True):
        # check input
        if isinstance(root, om.MDagPath):
            self.root_node: om.MDagPath = root
        elif isinstance(root, str):
            self.root_node: om.MDagPath = om.MSelectionList().add(root).getDagPath(0)
        else:
            raise Exception("Invalid root node, must be a string or MDagPath.")

        self.skipShape = skipShape

        # result iterator list
        self._reset()

    def _reset(self):
        self.iterList = [self.root_node]

    def __iter__(self):
        self._reset()
        return self

    def __next__(self) -> Tuple[str, om.MDagPath]:
        if not self.iterList:
            raise StopIteration("End of iteration.")
        # get the current node
        current_dag = self.iterList.pop()
        # get the children
        children: om.MDagPath = []
        for x in range(current_dag.childCount()):
            mObj: om.MObject = current_dag.child(x)
            if (not mObj.hasFn(om.MFn.kTransform)) and self.skipShape:
                continue
            children.append(om.MDagPath.getAPathTo(mObj))

        self.iterList.extend(reversed(children))
        name: str = current_dag.partialPathName()
        dag: om.MDagPath = current_dag
        return name, dag


if __name__ == "__main__":
    for x, dag in IterHierarchy("Rig"):
        print(x)
        print(dag)
