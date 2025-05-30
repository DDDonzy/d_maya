# Author:   Donzy.xu
# CreateTime:   2023/2/16 - 16:29
# FileName:  namespace.py


import maya.cmds as cmds
from UTILS.ui.showMessage import showMessage


def removeNamespace():
    system_namespace_list = ['UI', 'shared']
    namespace_list = cmds.namespaceInfo(":", lon=True)
    namespace_list = list(set(namespace_list) ^ set(system_namespace_list))

    while len(namespace_list) > 0:
        cmds.namespace(rm=namespace_list[0], mnr=1)
        namespace_list = cmds.namespaceInfo(":", lon=True)
        namespace_list = list(set(namespace_list) ^ set(system_namespace_list))
    showMessage("REMOVE_NAMESPACE")

# removeNamespace()
