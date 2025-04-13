from maya.api import OpenMaya as om


class iterHierarchy(object):
    def __init__(self, rootDag, shape=True):
        # check input
        if isinstance(rootDag, om.MDagPath):
            self.root_node = rootDag
        elif isinstance(rootDag, str):
            self.root_node = om.MSelectionList().add(rootDag).getDagPath(0)
        else:
            raise Exception("Invalid root node, must be a string or MDagPath.")

        self.shape = shape

        # result iterator list
        self._reset()

    def _reset(self):
        self.iterList = [self.root_node]

    def __iter__(self):
        self._reset()
        return self

    def __next__(self):
        if not self.iterList:
            raise StopIteration("End of iteration.")
        # get the current node
        current_dag = self.iterList.pop()
        # get the children
        children = []
        for x in range(current_dag.childCount()):
            mObj = current_dag.child(x)
            if (not mObj.hasFn(om.MFn.kTransform)) and (not self.shape):
                continue
            children.append(om.MDagPath.getAPathTo(mObj))

        self.iterList.extend(reversed(children))
        name: str = current_dag.partialPathName()
        dag: om.MDagPath = current_dag
        return name, dag
