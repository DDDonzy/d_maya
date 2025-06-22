from maya import cmds


def prune_small_weights(skinClusterNode: str = None, pruneWeights: float = 0.001):
    if skinClusterNode is None:
        skinClusterNode = cmds.ls(type="skinCluster")
    if isinstance(skinClusterNode, str):
        skinClusterNode = [skinClusterNode]

    for x in skinClusterNode:
        try:
            shapes = cmds.skinCluster(x, q=1, g=1)
            for shape in shapes:
                cmds.skinPercent(x, shape, prw=pruneWeights)
                print(f"PRUNE SMALL WEIGHTS: {shape}")
        except RuntimeError:
            print(f"ERROR PRUNE SMALL WEIGHTS : {shape}")


if __name__ == "__main__":
    prune_small_weights(0.001)
