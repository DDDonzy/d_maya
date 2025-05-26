import re
from maya import cmds


def generateUniqueName(name):
    """
    Generate a unique name by adding numeric suffix if the base name already exists

    Args:
        name (str): The base name to start with

    Returns:
        str: A unique name that doesn't exist in the scene

    """
    while cmds.objExists(name):
        # Find trailing digits: matches numbers at the end (ignoring non-digits after)
        # Example: "object123abc" matches "123"
        match = re.search(r'(\d+)(?=[^0-9]*$)', string=name)
        if match:
            indexStr = match.group(0)
            indexInt = int(indexStr) + 1
            # Keep zero-padding format: "001" -> "002"
            indexStr = f"{indexInt:0{len(indexStr)}}"
            # Replace the found digits with incremented number
            name = re.sub(r'(\d+)(?=[^0-9]*$)', indexStr, name)
        else:
            # No digits found, append "1"
            name = f"{name}{1}"
    return name


def adjustName(name, baseName='', num=1):
    """
    Rationalized name
    Args:
        name (str): The name to rationalize
        baseName (str): The base name to replace @ placeholder
        num (int): The number to replace # placeholder

    Returns:
        str: A rationalized name following Maya naming conventions
    """
    if not name:
        return name
    
    # Replace invalid characters with underscore (keep only letters, digits, _, #, @)
    name = re.sub(r'[^a-zA-Z0-9_#@]', '_', string=name)
    
    # Replace @ placeholder with baseName
    name = re.sub(r"\@", f"{baseName}", name)
    
    # Replace # placeholder with number
    name = re.sub(r"\#", f"{num}", name)
    
    # Merge multiple underscores into single underscore
    name = re.sub(r'_{2,}', '_', name)
    
    # Remove leading underscore
    if name[0] == "_":
        name = name[1:]
    
    # Add underscore if starts with digit (Maya requirement)
    if name[0].isdigit():
        name = "_" + name
    
    # Remove trailing underscore
    if name[-1] == "_":
        name = name[0:-1]
    
    return name
