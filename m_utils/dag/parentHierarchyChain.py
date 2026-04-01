import maya.cmds as cmds
from maya.api import OpenMaya as om

def parent_hierarchy_chain(selection=None):
    # If no selection is provided by the user, fallback to getting the current Maya selection.
    # 'orderedSelection=True' ensures the list strictly follows the user's selection order.
    if not selection:
        selection = cmds.ls(orderedSelection=True) or []

    # Check if at least two objects are selected or provided.
    if len(selection) < 2:
        om.MGlobal.displayError("Failed to create hierarchy chain: Please provide or select at least two objects in order!")
        return

    # Keep track of the current parent node. 
    # This is crucial because a node's full path/name changes after it is parented.
    current_parent = selection[0]

    # Iterate through the list, starting from the second object (index 1).
    for i in range(1, len(selection)):
        child = selection[i]

        try:
            # Parent the child to the current parent.
            # cmds.parent returns a list of the new names/paths of the parented objects.
            new_child_name = cmds.parent(child, current_parent)[0]
            
            # The newly parented child becomes the parent for the next object in the chain.
            current_parent = new_child_name
        except Exception as e:
            om.MGlobal.displayWarning(f"Could not parent '{child}' to '{current_parent}'. Reason: {e}")
            # Fallback to the original name if parenting failed, to keep the loop going safely
            current_parent = child

    # Clear selection.
    cmds.select(clear=True)


if __name__ == "__main__":
    parent_hierarchy_chain()
