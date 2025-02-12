def createMeshBase(name: str):
    print(f"create {name}")


def createMesh(name):
    if isinstance(name, str):
        name = [name]
    for x in name:
        createMeshBase(x)
        
