from maya import cmds


def generateUniqueName(base_name):
    """
    Generate a unique name by adding numeric suffix if the base name already exists

    Args:
        base_name (str): The base name to start with

    Returns:
        str: A unique name that doesn't exist in the scene

    """
    name = base_name
    index = 1

    while cmds.objExists(name):
        name = f"{base_name}{index}"
        index += 1

    return name
