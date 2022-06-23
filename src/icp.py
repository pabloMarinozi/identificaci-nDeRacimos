import numpy as np
import open3d as o3d
import copy

def icp_search(source, target, neighbors_distance, step=np.pi / 3, presicion_target=0.0001):
    # source.translate((0, 0, 0), relative=False)
    # target.translate((0, 0, 0), relative=False)
    # o3d.visualization.draw_geometries([cloud, rt_cloud])

    steps_number = int(2 * np.pi // step)
    lowest_icp_rmse = 100
    best_icp = None
    # best_icp.inlier_rmse = 100
    for x in range(steps_number):
        for y in range(steps_number):
            for z in range(steps_number):
                source_cp = copy.deepcopy(source)
                coords = (x * step, y * step, z * step)
                R_aux = source_cp.get_rotation_matrix_from_xyz(coords)
                source_cp.rotate(R_aux)
                icp = o3d.pipelines.registration.registration_icp(source_cp, target, neighbors_distance)
                e = icp.inlier_rmse
                fitness = icp.fitness
                itn = x * 13 ** 2 + y * 13 + z + 1
                if e < lowest_icp_rmse and fitness > 0.7:
                    lowest_icp_rmse = e
                    best_icp = icp
                    R = R_aux
                # if e < presicion_target:
                #     # o3d.visualization.draw_geometries([target, source_cp.transform(icp.transformation)])
                #     return best_icp, R, itn
    return best_icp, R, itn