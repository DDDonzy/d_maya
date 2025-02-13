import re
from maya import cmds


def generateUniqueName(name):
    while cmds.objExists(name):
        match = re.search(r'(\d+)(?=[^0-9]*$)', string=name)
        if match:
            indexStr = match.group(0)
            indexInt = int(indexStr) + 1
            indexStr = "%0*d" % (len(indexStr), indexInt)
            name = re.sub(r'(\d+)(?=[^0-9]*$)', indexStr, name)
        else:
            name = "{}{}".format(name, 1)
    return name


def adjustName(name, baseName='', num=1):
    if not name:
        return name
    name = re.sub(r'[^a-zA-Z0-9_#@]', '_', string=name)
    name = re.sub(r"\@", "{}".format(baseName), name)
    name = re.sub(r"\#", "{}".format(num), name)
    name = re.sub(r'_{2,}', '_', name)
    if name[0] == "_":
        name = name[1:]
    if name[0].isdigit():
        name = "_" + name
    if name[-1] == "_":
        name = name[0:-1]
    return name
