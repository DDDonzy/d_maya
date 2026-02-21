from maya import cmds

# build clip
main = cmds.ls("Main", r=1)
if not main:
    raise BaseException("Can not find 'Main' Controls")
cmds.select(main)
cmds.TimeEditorCreateClip()

start = 0
end = 0
for clip in cmds.ls("*.clip[*].clipStart"):
    _start = cmds.getAttr(clip)
    print(_start)
    if _start < start:
        start = _start

for clip in cmds.ls("*.clip[*].clipDuration"):
    _end = cmds.getAttr(clip)
    if _end > end:
        end = _end

cmds.playbackOptions(min=start, max=end)
