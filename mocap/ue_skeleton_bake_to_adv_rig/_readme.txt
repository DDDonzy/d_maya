1.动捕文件，通过fbx批量工具，重命名为ue的骨骼命名 （这环节可以省略，但是为了在ue中retarget 方便，建议这一步）（FBX文件下有映射json文件）
2.ue中使用 动作捕捉骨骼，重定向到 ue角色骨骼上
3.导出ue角色重定向后的动画
4.mayapy 运行run_maya_bakeAnimation.py 把重定向后的动画，烘焙到adv绑定上。