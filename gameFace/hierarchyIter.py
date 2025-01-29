from maya.api import OpenMaya as om


class hierarchyIter:
    def __init__(self, root_node, skipShape=False):
        self.skipShape = skipShape
        if isinstance(root_node, om.MDagPath):
            self.root_node = root_node
        elif isinstance(root_node, str):
            self.root_node = om.MSelectionList().add(root_node).getDagPath(0)
        self.stack = []
        self._reset()

    def _reset(self):
        self.stack = [self.root_node]

    def __iter__(self):
        self._reset()
        return self

    def __next__(self):
        if not self.stack:
            raise StopIteration
        current_node = self.stack.pop()
        children = []

        for x in range(current_node.childCount()):
            mObj = current_node.child(x)

            if not mObj.hasFn(om.MFn.kTransform):
                if self.skipShape:
                    continue
            children.append(om.MDagPath.getAPathTo(mObj))
        self.stack.extend(reversed(children))
        return current_node.partialPathName(), current_node
