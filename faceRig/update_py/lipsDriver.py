import maya.cmds as cmds
def addLipsDriver():
    jaw = 'M_JawLower_Position_CTL'
    L_lipCorner = 'L_LipConner_00_Gross_CTL'
    R_lipCorner = 'R_LipConner_00_Gross_CTL'
    cmds.addAttr(jaw , ln = '__' , nn = '_______' , at = 'enum',en='driverSets',k=1)
    cmds.setAttr(jaw+'.__' , l =1)
    cmds.addAttr(jaw , ln = 'jawMin' , at = 'double' , dv = -10 , k=1)
    cmds.addAttr(jaw , ln = 'jawMax' , at = 'double' , dv = 30 , k=1)
    cmds.setAttr(jaw+'.jawMin' , cb =1)
    cmds.setAttr(jaw+'.jawMax' , cb =1)
    jawMin_setRange = cmds.createNode('setRange' , name = jaw+'_jawMin_setRange')
    jawMax_setRange = cmds.createNode('setRange' , name = jaw+'_jawMax_setRange')
    cmds.connectAttr(jaw+'.jawMin' , jawMin_setRange+'.oldMinX')
    cmds.connectAttr(jaw+'.jawMax' , jawMax_setRange+'.oldMaxX')
    cmds.setAttr(jawMin_setRange+'.minX' , 1)
    cmds.setAttr(jawMax_setRange+'.maxX' , 1)
    cmds.addAttr(jaw , ln = 'jawMin_dr' , at = 'double' , dv = -10 , k=1)
    cmds.addAttr(jaw , ln = 'jawMax_dr' , at = 'double' , dv = -10 , k=1)
    cmds.connectAttr(jawMin_setRange + '.outValueX' , jaw+'.jawMin_dr')
    cmds.connectAttr(jawMax_setRange + '.outValueX' , jaw+'.jawMax_dr')
    cmds.setAttr(jaw+'.jawMin_dr',l=1)
    cmds.setAttr(jaw+'.jawMax_dr',l=1)
    cmds.connectAttr(jaw+'.rx' , jawMin_setRange+'.valueX')
    cmds.connectAttr(jaw+'.rx' , jawMax_setRange+'.valueX')
    for x in [L_lipCorner,R_lipCorner]:
        cmds.addAttr(x , ln = '__' , nn = '_______' , at = 'enum',en='driverSets',k=1)
        cmds.setAttr(x+'.__',l=1)
        cmds.addAttr(x , ln = 'txMin'  , at = 'double',k=1,dv = -1)
        cmds.addAttr(x , ln = 'txMax'  , at = 'double',k=1,dv = 1)
        cmds.addAttr(x , ln = 'tyMin'  , at = 'double',k=1,dv = -1)
        cmds.addAttr(x , ln = 'tyMax'  , at = 'double',k=1,dv = 1)
        cmds.setAttr(x+'.txMin',e=1,channelBox=1)
        cmds.setAttr(x+'.txMax',e=1,channelBox=1)
        cmds.setAttr(x+'.tyMin',e=1,channelBox=1)
        cmds.setAttr(x+'.tyMax',e=1,channelBox=1)
        x_min_setRange = cmds.createNode('setRange',name = x+'_x_min_driverSetRange')
        y_min_setRange = cmds.createNode('setRange',name = x+'_y_min_driverSetRange')
        x_max_setRange = cmds.createNode('setRange',name = x+'_x_max_driverSetRange')
        y_max_setRange = cmds.createNode('setRange',name = x+'_y_max_driverSetRange')
        cmds.connectAttr(x+'.txMin' , x_min_setRange+'.oldMinX')
        cmds.connectAttr(x+'.txMax' , x_max_setRange+'.oldMaxX')
        cmds.connectAttr(x+'.tyMin' , y_min_setRange+'.oldMinX')
        cmds.connectAttr(x+'.tyMax' , y_max_setRange+'.oldMaxX')
        cmds.setAttr(x_min_setRange+'.minX' , 1)
        cmds.setAttr(y_min_setRange+'.minX' , 1)
        cmds.setAttr(x_max_setRange+'.maxX' , 1)
        cmds.setAttr(y_max_setRange+'.maxX' , 1)
        cmds.addAttr(x , ln = 'inner'  , at = 'double',k=1,dv = -1)
        cmds.addAttr(x , ln = 'outer'  , at = 'double',k=1,dv = 1)
        cmds.addAttr(x , ln = 'lower'  , at = 'double',k=1,dv = -1)
        cmds.addAttr(x , ln = 'upper'  , at = 'double',k=1,dv = 1)
        cmds.connectAttr(x_min_setRange+'.outValueX' , x+'.inner')
        cmds.connectAttr(y_min_setRange+'.outValueX' , x+'.lower')
        cmds.connectAttr(x_max_setRange+'.outValueX' , x+'.outer')
        cmds.connectAttr(y_max_setRange+'.outValueX' , x+'.upper')
        cmds.connectAttr(x+'.tx' , x_min_setRange+'.valueX')
        cmds.connectAttr(x+'.tx' , x_max_setRange+'.valueX')
        cmds.connectAttr(x+'.ty' , y_min_setRange+'.valueX')
        cmds.connectAttr(x+'.ty' , y_max_setRange+'.valueX')
        cmds.setAttr(x+'.inner' , l=1)
        cmds.setAttr(x+'.outer' , l=1)
        cmds.setAttr(x+'.lower' , l=1)
        cmds.setAttr(x+'.upper' , l=1)
        cmds.addAttr(x , ln = 'outerUpper'  , at = 'double',k=1,dv = 1)
        cmds.addAttr(x , ln = 'outerLower'  , at = 'double',k=1,dv = 1)
        outerUpper = cmds.createNode('multDoubleLinear' , name = x+'_outerUpper')
        outerLower = cmds.createNode('multDoubleLinear' , name = x+'_outerLower')
        cmds.connectAttr(x+'.outer' , outerUpper+'.input1')
        cmds.connectAttr(x+'.upper' , outerUpper+'.input2')
        cmds.connectAttr(outerUpper+'.output' , x+'.outerUpper')
        cmds.connectAttr(x+'.outer' , outerLower+'.input1')
        cmds.connectAttr(x+'.lower' , outerLower+'.input2')
        cmds.connectAttr(outerLower+'.output' , x+'.outerLower')
        cmds.setAttr(x+'.outerUpper' , l=1)
        cmds.setAttr(x+'.outerLower' , l=1)
        cmds.addAttr(x , ln = 'openUpper' , at = 'double' , dv = 0 , k=1)
        cmds.addAttr(x , ln = 'openLower' , at = 'double' , dv = 0 , k=1)
        cmds.addAttr(x , ln = 'openInner' , at = 'double' , dv = 0 , k=1)
        cmds.addAttr(x , ln = 'openOuter' , at = 'double' , dv = 0 , k=1)
        cmds.addAttr(x , ln = 'openOuterUpper' , at = 'double' , dv = 0 , k=1)
        cmds.addAttr(x , ln = 'openOuterLower' , at = 'double' , dv = 0 , k=1)
        OU = cmds.createNode('multDoubleLinear' , name = x+'_OU_multDoubleLinear')
        OL = cmds.createNode('multDoubleLinear' , name = x+'_OL_multDoubleLinear')
        OI = cmds.createNode('multDoubleLinear' , name = x+'_OI_multDoubleLinear')
        OO = cmds.createNode('multDoubleLinear' , name = x+'_OO_multDoubleLinear')
        OOU = cmds.createNode('multDoubleLinear' , name = x+'_OOU_multDoubleLinear')
        OOL = cmds.createNode('multDoubleLinear' , name = x+'_OOL_multDoubleLinear')
        #jaw+'.jawMax_dr'
        cmds.connectAttr(jaw+'.jawMax_dr' , OU+'.input1')
        cmds.connectAttr(x+'.upper' , OU+'.input2')
        cmds.connectAttr(OU+'.output' , x+'.openUpper')

        cmds.connectAttr(jaw+'.jawMax_dr' , OL+'.input1')
        cmds.connectAttr(x+'.lower' , OL+'.input2')
        cmds.connectAttr(OL+'.output' , x+'.openLower')

        cmds.connectAttr(jaw+'.jawMax_dr' , OI+'.input1')
        cmds.connectAttr(x+'.inner' , OI+'.input2')
        cmds.connectAttr(OI+'.output' , x+'.openInner')

        cmds.connectAttr(jaw+'.jawMax_dr' , OO+'.input1')
        cmds.connectAttr(x+'.outer' , OO+'.input2')
        cmds.connectAttr(OO+'.output' , x+'.openOuter')

        cmds.connectAttr(jaw+'.jawMax_dr' , OOU+'.input1')
        cmds.connectAttr(x+'.outerUpper' , OOU+'.input2')
        cmds.connectAttr(OOU+'.output' , x+'.openOuterUpper')

        cmds.connectAttr(jaw+'.jawMax_dr' , OOL+'.input1')
        cmds.connectAttr(x+'.outerLower' , OOL+'.input2')
        cmds.connectAttr(OOL+'.output' , x+'.openOuterLower')
        cmds.setAttr(x+'.openUpper' , l=1)
        cmds.setAttr(x+'.openLower' , l=1)
        cmds.setAttr(x+'.openInner' , l=1)
        cmds.setAttr(x+'.openOuter' , l=1)
        cmds.setAttr(x+'.openOuterUpper' , l=1)
        cmds.setAttr(x+'.openOuterLower' , l=1)
addLipsDriver()