"""
Maya Asset Container Management with Context Manager
==================================================

This module provides a context manager for creating and managing Maya asset containers.
It supports both regular containers and DAG containers with automatic node organization.

Features:
- Context manager for automatic container creation and cleanup
- Support for nested containers with stack management
- Automatic parenting of DAG nodes to container
- Configurable container properties (blackBox, icon, etc.)
- Asset data publishing capabilities


Usage:
    with AssetCallback(name="myAsset", isDagAsset=True) as asset:
        cmds.polyCube(name="cube1")
        cmds.polySphere(name="sphere1")
    # All created nodes are automatically added to the container
"""


from maya import cmds


class AssetCallback:
    """
    Context manager for Maya asset container creation and management.
    
    This class provides automatic container creation, node management, and cleanup
    through Python's context manager protocol (__enter__ and __exit__).

    """
    asset_stack = []

    def __init__(self,
                 name: str = "asset",
                 parent: str = None,
                 isDagAsset: bool = True,
                 isBlackBox: bool = False,
                 icon: str = None,
                 force: bool = True):
        """
        Initialize the AssetCallback context manager.
        
        Args:
            name (str): Name for the container asset
            parent (str): Parent container to nest this asset under
            isDagAsset (bool): Create DAG container if True, regular container if False
            isBlackBox (bool): Set container as black box (hide internal connections)
            icon (str): Icon name for the container display
            force (bool): Force creation even if container with same name exists
        """
        self.parent = parent
        self.currentContainer = None
        self.lastContainer = None
        self.name = name
        self.force = force
        self.icon = icon
        self.blackBox = isBlackBox
        self.isDagAsset = isDagAsset

    def __enter__(self):
        """
        Enter the context manager - create container and set as current.
        
        Returns:
            AssetCallback: Self instance for use in 'with' statement
        """
        # Store reference to previous container in stack
        self.lastContainer = AssetCallback.asset_stack[-1] if AssetCallback.asset_stack else None
        
        # Create new container with specified parameters
        self.currentContainer = AssetCallback.createContainer(name=self.name,
                                                              isDagAsset=self.isDagAsset,
                                                              isBlackBox=self.blackBox,
                                                              icon=self.icon,
                                                              force=self.force)
        self.name = self.currentContainer
        
        # Set container as current (nodes created will be added to it)
        cmds.container(self.currentContainer, e=1, c=True)
        
        # Add to stack for nested container support
        AssetCallback.asset_stack.append(self)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Restore previous container as current or disable current container
        if self.lastContainer:
            cmds.container(self.lastContainer, e=1, c=True)
        else:
            cmds.container(self.currentContainer, e=1, c=False)
            # Add to parent container if specified
            if self.parent:
                cmds.container(self.parent, e=1, an=[self])

        # For DAG containers, organize hierarchy by parenting orphaned nodes
        if self.isDagAsset:
            nodeList = cmds.container(self.currentContainer, q=1, nodeList=1) or []
            for x in nodeList:
                if cmds.objectType(x, isAType="transform"):
                    # Check if node's parent is outside the container
                    if (cmds.listRelatives(x, p=1) or ["world"])[0] not in nodeList+[self.currentContainer]:
                        # Parent the node to the container
                        cmds.parent(x, self.currentContainer)

        # Remove from stack
        AssetCallback.asset_stack.pop()

    def __repr__(self):
        """String representation of the container."""
        return str(self.currentContainer)

    def __str__(self):
        """String conversion of the container."""
        return str(self.currentContainer)

    @staticmethod
    def createContainer(name: str,
                        isDagAsset: bool = True,
                        isBlackBox: bool = False,
                        icon: str = None,
                        force: bool = True):
        """
        Create a Maya container with specified properties.
        
        Args:
            name (str): Container name
            isDagAsset (bool): Create DAG container if True
            isBlackBox (bool): Set as black box container
            icon (str): Icon name for display
            force (bool): Force creation if name exists
            
        Returns:
            str: Name of created container
        """
        # Return existing container if force is False and it exists
        if not force and cmds.objExists(name):
            return name
            
        assetType = ("container", "dagContainer")[isDagAsset]
        container = cmds.createNode(assetType, name=name, skipSelect=True)
        
        cmds.container(container, e=1, addNode=[])
        cmds.setAttr(f"{container}.blackBox", isBlackBox) if isBlackBox else None
        cmds.setAttr(f"{container}.iconName", icon, type="string") if icon else None
        cmds.setAttr(f"{container}.viewMode", 0)
        
        return container

    @staticmethod
    def publishAssetData(name: str,
                         isPublishAssetAttr: bool = False,
                         publishAttrData: dict = None,
                         isPublishNode: bool = False,
                         publishNodeList: list = []):
        """
        Publish asset data for external access.
        
        Args:
            name (str): Container name to publish data for
            isPublishAssetAttr (bool): Enable attribute publishing
            publishAttrData (dict): Dictionary of attributes to publish
            isPublishNode (bool): Enable node publishing
            publishNodeList (list): List of nodes to publish
        """
        # Publish attributes if requested
        if publishAttrData and isPublishAssetAttr:
            if publishAttrData and isinstance(publishAttrData, dict):
                for k, v in publishAttrData.items():
                    cmds.container(name, e=1, publishAndBind=[v, k])
                    
        # Publish nodes if requested
        if publishNodeList and isPublishNode:
            if publishNodeList and isinstance(publishNodeList, list):
                for x in publishNodeList:
                    cmds.containerPublish(name, publishNode=[x, ""])
                    cmds.containerPublish(name, bindNode=[x, x])


if __name__ == "__main__":
    # Example usage: Create a container and add geometry to it
    with AssetCallback(name="testAsset") as asset:
        cmds.polyCube(name="testCube")
        cmds.polySphere(name="testSphere")
        cmds.group(name="testGroup")
        cmds.joint(name="testJoint")