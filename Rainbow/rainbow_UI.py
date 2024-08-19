import maya.cmds as cmds
import maya.mel as mel
import os,sys
sys.path.append(os.path.dirname(__file__))
def current_path():
    path = os.path.dirname(__file__)
    return path

def rainbow_win():
    if cmds.window('rainbow_win', exists=True): cmds.deleteUI('rainbow_win')
    if cmds.windowPref('rainbow_win', exists=True): cmds.windowPref('rainbow_win', remove=True)

    cmds.window('rainbow_win', wh=(406, 610), t='Rainbow')

    mainLayout = cmds.paneLayout(configuration='horizontal2',ps = (1,100,68))

    curve_frame = cmds.frameLayout(label='Curves', p=mainLayout)

    cmds.scrollLayout(childResizable=1, p=curve_frame)
    cmds.gridLayout(numberOfColumns=8, cellWidthHeight=(50, 50))
    curve_grid()

    cmds.rowLayout(p=curve_frame,nc = 3,cw3 = (300,50,50),cat = [(2,'left',10), (3,'left',5)])
    cmds.floatSliderGrp('scale_slider', label='Scale : ', field=True, minValue=0, maxValue=1,  value=0.2 ,cw3 = (50,50,200),cat = (3,'both',5))
    cmds.iconTextButton('sub_scale_button', image1='addClip.png', c = 'curve_scale(0)')
    cmds.iconTextButton('add_scale_button', image1='addClip.png', c = 'curve_scale(1)')

    #cmds.separator(p = curve_frame)
    color_frame = cmds.frameLayout(label='Colors', p=mainLayout)
    cmds.scrollLayout(childResizable=1, p=color_frame)
    cmds.gridLayout(numberOfColumns=8, cellWidthHeight=(50, 40))
    for i in range(32):
        cmds.canvas(rgbValue=canvas_color(i),pc = 'change_color({})'.format(i))

    cmds.showWindow('rainbow_win')

def change_color(index):
    sel = cmds.ls(sl =True)
    for i in sel:
        shapes = cmds.listRelatives(i, f=True, s=True)
        for shape in shapes:
            cmds.setAttr('{}.overrideEnabled'.format(shape), 1)
            cmds.setAttr('{}.overrideColor'.format(shape), index)

def curve_grid():
    libpath = r'{}/lib'.format(current_path())
    lib = os.listdir(libpath)

    curve_name = []
    curve_shape = {}
    curve_img = {}

    for data in lib:
        if data.split('.')[-1] == 'cs':
            name = data.split('.')[0]
            curve_name.append(name)
            curve_shape[name] = data
            img = ('{}/{}_icon_L.bmp'.format(libpath, data.split('.')[0]))
            curve_img[name] = img

    for icon in curve_name:
        cmds.iconTextButton(style='iconOnly', image1=curve_img[icon], label='', c='create_curve(0,"{}")'.format(icon),
                            dcc='create_curve(1,"{}")'.format(icon))



def create_curve(mod, name):
    libpath = r'{}/lib'.format(current_path())


    with open('{}/{}.cs'.format(libpath, name), 'r') as f:
        shape = f.read()
        if mod == 0:
            rainbow = cmds.createNode('transform', n='rainbow')
            cmds.createNode('nurbsCurve', n='rainbowShape', p=rainbow)
            mel.eval(shape)
            cmds.select(rainbow, r=True)

        else:
            sel = cmds.ls(sl=True)
            for i in sel:
                type = cmds.listRelatives(i, f=True, s=True)
                for t in type:                    
                    if  not cmds.objectType(t) == 'nurbsCurve':
                        cmds.error('Not a nurbsCurve : {}'.format(i))
            for i in sel:
                old_shape = cmds.listRelatives(i, f=True, s=True)
                old_enabled = cmds.getAttr('{}.overrideEnabled'.format(old_shape[0]))
                old_color = cmds.getAttr('{}.overrideColor'.format(old_shape[0]))
                
                cmds.delete(old_shape)

                new_shape = cmds.createNode('nurbsCurve', n='{}Shape'.format(i), p=i)
                mel.eval(shape)
                if old_enabled:
                    cmds.setAttr('{}.overrideEnabled'.format(new_shape), 1)
                    cmds.setAttr('{}.overrideColor'.format(new_shape), old_color)
            cmds.select(sel, r=True)

def curve_scale(mod):
    rate = cmds.floatSliderGrp('scale_slider',q = True, value = True)

    sel = cmds.ls(sl = True)
    for i in sel:
        cmds.select('{}.cv[*]'.format(i),r = True)
        if mod == 0:
            cmds.scale((1-rate),(1-rate),(1-rate), r = True)
        else:
            cmds.scale((1+rate),(1+rate),(1+rate), r = True)
    cmds.select(sel, r = True)


def canvas_color(index):
    if index == 0:
        return (0.627, 0.627, 0.627)

    elif index == 1:
        return (0, 0, 0)

    elif index == 2:
        return (0.247, 0.247, 0.247)

    elif index == 3:
        return (0.498, 0.498, 0.498)

    elif index == 4:
        return (0.608, 0, 0.157)

    elif index == 5:
        return (0, 0.016, 0.373)

    elif index == 6:
        return (0, 0, 1)

    elif index == 7:
        return (0, 0.275, 0.094)

    elif index == 8:
        return (0.145, 0, 0.263)

    elif index == 9:
        return (0.78, 0, 0.78)

    elif index == 10:
        return (0.537, 0.278, 0.2)

    elif index == 11:
        return (0.243, 0.133, 0.122)

    elif index == 12:
        return (0.6, 0.145, 0)

    elif index == 13:
        return (1, 0, 0)

    elif index == 14:
        return (0, 1, 0)

    elif index == 15:
        return (0, 0.255, 0.6)

    elif index == 16:
        return (1, 1, 1)

    elif index == 17:
        return (1, 1, 0)

    elif index == 18:
        return (0.388, 0.863, 1)

    elif index == 19:
        return (0.263, 1, 0.635)

    elif index == 20:
        return (1, 0.686, 0.686)

    elif index == 21:
        return (0.89, 0.675, 0.475)

    elif index == 22:
        return (1, 1, 0.384)

    elif index == 23:
        return (0, 0.6, 0.325)

    elif index == 24:
        return (0.627, 0.412, 0.188)

    elif index == 25:
        return (0.62, 0.627, 0.188)

    elif index == 26:
        return (0.408, 0.627, 0.188)

    elif index == 27:
        return (0.188, 0.627, 0.365)

    elif index == 28:
        return (0.188, 0.627, 0.627)

    elif index == 29:
        return (0.188, 0.404, 0.627)

    elif index == 30:
        return (0.435, 0.188, 0.627)

    else:
        return (0.627, 0.188, 0.412)


