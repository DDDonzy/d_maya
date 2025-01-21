import maya.standalone
maya.standalone.initialize()


from maya import cmds
from UTILS.transform import transform as t
import cProfile

print("MAYA RUN!")

cmds.file(r"C:/Users/ext.dxu/Desktop/cprofile.ma", o=1)

print("OPEN !")


source = "pSphere1"
target = ['pCube1', 'pCube2', 'pCube3', 'pCube4', 'pCube5', 'pCube25', 'pCube26', 'pCube23', 'pCube30', 'pCube22', 'pCube34', 'pCube16', 'pCube19', 'pCube17', 'pCube18', 'pCube13', 'pCube10', 'pCube11', 'pCube9', 'pCube39',
          'pCube21', 'pCube24', 'pCube32', 'pCube31', 'pCube33', 'pCube29', 'pCube28', 'pCube38', 'pCube40', 'pCube27', 'pCube8', 'pCube6', 'pCube7', 'pCube20', 'pCube15', 'pCube12', 'pCube14', 'pCube35', 'pCube37', 'pCube36']


profiler = cProfile.Profile()
profiler.enable()  # 开始性能分析

t.matrixConstraint(source, *target)

profiler.disable()  # 停止性能分析

# 输出性能分析报告
profiler.print_stats()
