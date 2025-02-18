# max
for x in range(10):
    uv = [0, 0]
    faceIndex = 0
    uvPin = "Sphere001"
    
    maxScript = """
    uv = {0}
    faceIndex = {1}
    uvPin = ${2}

    ctl = Point()
    ctl.cross = True
    ctl.wireColor = color 50 120 20

    attachController = Attachment()
    ctl.pos.controller = attachController
    attachController.node = uvPin
    attachController.align = true

    keyNew = AttachCtrl.addNewKey attachController 0
    keyNew.face = faceIndex
    keyNew.coord = uv
    """.format(uv,faceIndex,uvPin)

    pymxs.runtime.execute(maxScript)
