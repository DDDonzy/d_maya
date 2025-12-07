from maya.api import OpenMaya as om
from maya import cmds

def orient_joint(joint_list: list,
                 first_axis: str = "x",
                 first_axis_neg: bool = False,
                 second_axis: str = "y",
                 second_axis_neg: bool = False,
                 ref_axis: str = "y",
                 ref_axis_neg: bool = False):

    axis_dict = {"x": (1, 0, 0),
                 "y": (0, 1, 0),
                 "z": (0, 0, 1)}

    # radians to euler
    def radians_to_degrees(euler):
        return [om.MAngle(r).asDegrees() for r in euler]

    # set transform
    def orient_transform(matrix):
        world_matrix[0] = matrix
        for i, m in enumerate(world_matrix):
            if i == 0:
                local_matrix = m * parent_matrix_inverse[i]
            else:
                local_matrix = m * world_matrix[0].inverse()
            transformation_matrix = om.MTransformationMatrix(local_matrix)
            euler = transformation_matrix.rotation()
            euler = radians_to_degrees([euler.x, euler.y, euler.z])
            translate = transformation_matrix.translation(1)
            obj = dag_path[i].fullPathName()
            cmds.setAttr(f"{obj}.translate", *translate)
            cmds.setAttr(f"{obj}.jointOrient", *euler)
            cmds.setAttr(f"{obj}.rotate", *(0, 0, 0))

    # cal offset matrix by input
    first_axis_vector = om.MVector(axis_dict.get(first_axis, (1, 0, 0)))
    second_axis_vector = om.MVector(axis_dict.get(second_axis, (0, 1, 0)))
    third_axis_vector = first_axis_vector ^ second_axis_vector
    second_axis_vector = third_axis_vector ^ first_axis_vector
    offset_matrix = om.MMatrix([[first_axis_vector.x, first_axis_vector.y, first_axis_vector.z, 0],
                               [second_axis_vector.x, second_axis_vector.y, second_axis_vector.z, 0],
                               [third_axis_vector.x, third_axis_vector.y, third_axis_vector.z, 0],
                               [0, 0, 0, 1]]).inverse()

    # get data--- API >>> SelectionList >>> Dag >> Matrix
    selection_list = om.MSelectionList()
    for jnt in joint_list:
        selection_list.add(jnt)
    dag_path = [selection_list.getDagPath(i) for i in range(selection_list.length())]
    world_matrix = [dag.inclusiveMatrix() for dag in dag_path]
    parent_matrix_inverse = [dag.exclusiveMatrixInverse() for dag in dag_path]

    # if no children use parent rotate
    if len(world_matrix) <= 1:
        orient_matrix = parent_matrix_inverse[0].inverse()
        orient_matrix[12], orient_matrix[13], orient_matrix[14] = world_matrix[0][12], world_matrix[0][13], world_matrix[0][14]
        orient_transform(orient_matrix)
        return

    # get matrix and position
    jnt_matrix = world_matrix[0]
    end_matrix = world_matrix[1]
    jnt_pos = om.MVector(jnt_matrix[12], jnt_matrix[13], jnt_matrix[14])
    end_pos = om.MVector(end_matrix[12], end_matrix[13], end_matrix[14])

    # first vector
    first_vector = (end_pos - jnt_pos).normalize()
    if first_axis_neg:
        first_vector *= -1

    # use quad rotate to orient joint
    if second_axis not in "xyz" or ref_axis not in "xyz":
        orig_first_vector = om.MVector(jnt_matrix[0], jnt_matrix[1], jnt_matrix[2])
        orig_second_vector = om.MVector(jnt_matrix[4], jnt_matrix[5], jnt_matrix[6])
        orig_third_vector = om.MVector(jnt_matrix[8], jnt_matrix[9], jnt_matrix[10])
        # cal first axis rotate quad
        rotate_quad = orig_first_vector.rotateTo(first_vector).normalizeIt()
        # rotate second and third axis by quad
        second_vector = orig_second_vector.rotateBy(rotate_quad)
        third_vector = orig_third_vector.rotateBy(rotate_quad)
        # construct matrix
        orient_matrix = om.MMatrix([[first_vector.x, first_vector.y, first_vector.z, 0],
                                    [second_vector.x, second_vector.y, second_vector.z, 0],
                                    [third_vector.x, third_vector.y, third_vector.z, 0],
                                    [jnt_pos.x, jnt_pos.y, jnt_pos.z, 1]])
        orient_transform(orient_matrix)
        return
    # use ref axis to orient joint
    # ref vector
    ref_vector = om.MVector(axis_dict.get(ref_axis, (0, 1, 0)))
    if ref_axis_neg:
        ref_vector *= -1
    # third vector
    third_vector = (first_vector ^ ref_vector).normalize()
    if second_axis_neg:
        third_vector *= -1
    # second vector
    second_vector = (third_vector ^ first_vector).normalize()
    # construct matrix
    orient_matrix = om.MMatrix([[first_vector.x, first_vector.y, first_vector.z, 0],
                                [second_vector.x, second_vector.y, second_vector.z, 0],
                                [third_vector.x, third_vector.y, third_vector.z, 0],
                                [jnt_pos.x, jnt_pos.y, jnt_pos.z, 1]])
    orient_transform(offset_matrix * orient_matrix)