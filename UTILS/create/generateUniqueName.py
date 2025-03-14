import re
from maya import cmds


def generateUniqueName(name):
    """
    Generate a unique name by adding numeric suffix if the base name already exists

    Args:
        base_name (str): The base name to start with

    Returns:
        str: A unique name that doesn't exist in the scene

    """
    while cmds.objExists(name):
        match = re.search(r'(\d+)(?=[^0-9]*$)', string=name)
        if match:
            indexStr = match.group(0)
            indexInt = int(indexStr) + 1
            indexStr = f"{indexInt:0{len(indexStr)}}"
            name = re.sub(r'(\d+)(?=[^0-9]*$)', indexStr, name)
        else:
            name = f"{name}{1}"
    return name


def adjustName(name, baseName='', num=1):
    """
    Rationalized name
    Args:
        base_name (str): The base name to start with

    Returns:
        str: A unique name that doesn't exist in the scene
    """
    if not name:
        return name
    name = re.sub(r'[^a-zA-Z0-9_#@]', '_', string=name)
    name = re.sub(r"\@", f"{baseName}", name)
    name = re.sub(r"\#", f"{num}", name)
    name = re.sub(r'_{2,}', '_', name)
    if name[0] == "_":
        name = name[1:]
    if name[0].isdigit():
        name = "_" + name
    if name[-1] == "_":
        name = name[0:-1]
    return name
