import re
from enum import Enum
from PySide2.QtWidgets import QTreeView, QLabel
from PySide2.QtCore import QModelIndex


class SelectedItemType(Enum):
    blendShape_node = 1
    blendShape_group = 2
    blendShape_target = 3
    blendShape_targetGroup = 4
    blendShape_targetInbetween = 5


class TreeViewIterator:
    """
    # Iter QTreeView items

    Example:
        for idx in TreeViewIterator(treeView):
            item_text = get_treeViewItemText(treeView, idx)


    Parameters:
        treeView (QTreeView): the QTreeView instance to iterate over
    Returns:
        index (QModelIndex): index of the current item in the tree view
    """

    def __init__(self, treeView: QTreeView):
        self.tree_view = treeView
        self.model = treeView.model()

    def __iter__(self):
        root = self.model.invisibleRootItem()  # root item of the model
        # iterate all top-level items
        for i in range(root.rowCount()):
            child_item = root.child(i)
            if child_item:
                index = self.model.indexFromItem(child_item)
                yield from self._iter_recursive(index)

    def _iter_recursive(self, index):
        # iterate the children of the current index
        yield index
        item = self.model.itemFromIndex(index)
        if item:
            for i in range(item.rowCount()):
                child_item = item.child(i)
                if child_item:
                    child_index = self.model.indexFromItem(child_item)
                    yield from self._iter_recursive(child_index)


def _match_pattern(text, pattern):
    """ 
    # Check if the text matches the pattern. 

    Example:
        _match_pattern("pCube1", "p*ube*") -> True

    """
    pattern = pattern.replace("*", ".*")
    return bool(re.search(pattern, text, re.IGNORECASE))


def get_treeViewItemText(tree_view: QTreeView, index: QModelIndex):
    """Get the text of a tree view item."""
    try:
        item = tree_view.indexWidget(index)
        widgets = item.children()
        return widgets[1].text()
    except Exception as e:
        print(f"Error getting item text: {e}")
        return ""


def get_treeViewItemIconLabel(tree_view: QTreeView, index: QModelIndex):
    """Get the icon QLabel of a tree view item."""
    try:
        item = tree_view.indexWidget(index)
        widgets = item.children()
        return widgets[0]
    except Exception as e:
        print(f"Error getting icon QLabel: {e}")
        return None


def treeView_filter(treeView: QTreeView, filterStr: str = "", filterType: SelectedItemType = None):
    """
    # Filter treeView's items.

    Example:
        treeView_filter(tree_view, filter_str="bs_1", filter_type=SelectedItemType.blendShape_node)

    Args:
        tree_view (QTreeView): The QTreeView instance to filter.
        filter_str (str): Filter string, supports multiple keywords separated by '&'.
        filter_type (SelectedItemType): The type of items to filter. If None, uses default logic.

    Returns:
        None
    """

    if not treeView:
        return

    model = treeView.model()
    if not model:
        return

    filterable_items = []  # get all need to filter items
    parent_indices = set()  # save parent item's idx to show them later

    for index in TreeViewIterator(treeView):
        item = model.itemFromIndex(index)
        if not item:
            continue
        item_data = item.data()  # 1=bsNode, 2=bsGroup, 3=bsTarget, 4=bsTargetGroup, 5=bsTargetInbetween
        if not item_data:
            continue

        try:
            itemType = SelectedItemType(item_data)
        except (ValueError, TypeError):
            continue

        if (itemType.value < 3) and (not filterType):
            filterable_items.append((index, item, itemType))
            continue

        if itemType == filterType:
            filterable_items.append((index, item, itemType))

    # if no items to filter, show all
    if not filterStr:
        for index, _, _ in filterable_items:
            treeView.setRowHidden(index.row(), index.parent(), False)
        return

    # filter
    filterWorlds = filterStr.split("&")  # pCube1&pCube2 ----> ['pCube1', 'pCube2']
    for index, item, item_type in filterable_items:
        should_show = False

        name = get_treeViewItemText(treeView, index)
        if not name:
            continue

        if filterType == SelectedItemType.blendShape_node:  # bsNode types
            if name in filterWorlds:
                should_show = True

        else:  # bsTarget, bsTargetInbetween types
            # match = _match_pattern(name, filterStr) # is name matches the filterStr ?
            match = any([_match_pattern(name, f_str) for f_str in filterWorlds])  # is name matches any of the filterWorlds ?
            if match:
                should_show = True

        if should_show:  # item should be visible and get its all parent indices
            parent_index = index.parent()
            while parent_index.isValid():
                parent_indices.add(parent_index)
                parent_index = parent_index.parent()

        # set visibility for the item
        treeView.setRowHidden(index.row(), index.parent(), not should_show)

    # show all parent indices of the filtered items
    for parent_index in parent_indices:
        treeView.setRowHidden(parent_index.row(), parent_index.parent(), False)


if __name__ == "__main__":
    tree_view = QTreeView()  # 假设你有一个QTreeView实例
    filterNode = "bs_1"
    filterTarget = "target_1"
    treeView_filter(treeView=tree_view, filterStr=filterNode if not filterNode else "!@#$%^&*()", filterType=SelectedItemType(2))
    treeView_filter(treeView=tree_view, filterStr=filterNode, filterType=SelectedItemType(1))
    treeView_filter(treeView=tree_view, filterStr=filterTarget, filterType=SelectedItemType(3))
