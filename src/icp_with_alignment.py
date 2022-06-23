import copy
import random
import open3d as o3d
import numpy as np

def get_neighbors_generator(pc, n_neighbors):
    """type_flag: True return poincloud, False return np.array"""
    pc_tree = o3d.geometry.KDTreeFlann(pc)
    points = np.asarray(pc.points)
    # points = np.append(points, [[0, 0, 0]], axis=0)
    for point in points:
        _, idxs, _ = pc_tree.search_knn_vector_3d(point, n_neighbors + 1)
        yield points[idxs[0], :], points[idxs[1:], :]


def compare_distances(dist1, dist2, tolerance):
    lower_end = dist1 * (1 - tolerance)
    top_end = dist1 * (1 + tolerance)
    if lower_end < dist2 < top_end:
        return True
    else:
        return False


def get_RT_in_z_direction(point, neighbor, dist):
    A = np.asarray([[0., 0., 0.], [0., 0., dist]])
    B = np.asarray([point, neighbor])
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    Am = A - centroid_A
    Bm = B - centroid_B
    H = np.transpose(Am) @ Bm
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T
    # point_cloud_viewer([conform_point_cloud(Am), conform_point_cloud(np.dot(Bm, R))])
    return R, centroid_B


def icp_search_arround_z(source, target, neighbors_distance=0.8, step=np.pi / 10):
    steps_number = int(2 * np.pi // step)
    highest_icp_fitness = 0
    best_icp = None
    R = 0
    for z in range(steps_number):
        source_cp = copy.deepcopy(source)
        coords = (0, 0, z * step)
        R_aux = source_cp.get_rotation_matrix_from_xyz(coords)

        source_cp.rotate(R_aux, center=(0, 0, 0))
        # source_cp.paint_uniform_color([1, 0, 1])
        # mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
        # o3d.visualization.draw_geometries([target, source, mesh])
        # o3d.visualization.draw_geometries([target, source_cp, mesh])

        icp = o3d.pipelines.registration.registration_icp(source_cp, target, neighbors_distance)
        fitness_error = icp.fitness
        fitness = icp.fitness
        # print(icp)
        # itn = z + 1
        # point_cloud_viewer([target, source_cp.transform(icp.transformation)])
        # mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
        # o3d.visualization.draw_geometries([target, source_cp, mesh])
        if icp is not None:
            if fitness > highest_icp_fitness:
                highest_icp_fitness = fitness
                best_icp = icp
                R = R_aux
    return best_icp


def custom_roto_translate(pc, rot, translate):
    points = np.asarray(pc.points)
    points = points - translate
    points = np.dot(points, rot)
    pc.points = o3d.utility.Vector3dVector(points)

def get_overlap(idxs_1, idxs_2):
    overlap = 0
    for idx1 in idxs_1:
        for idx2 in idxs_2:
            if idx1 == idx2:
                overlap += 1
    return overlap


def icp_from_neighbors(source, target, threshold, n_neighbors, angle_step, distances_tolerance):
    """devuelve: (cantidad de matcheos, cantidad de puntos nube source, cantidad de puntos nube target, rmse, conjunto de correspondencia)"""
    highest_fitness = 0
    best_icp = None
    n_points_source = len(np.asarray(source.points))
    n_points_target = len(np.asarray(target.points))

    for point1, nn_points1 in get_neighbors_generator(target, n_neighbors):
        for point2, nn_points2 in get_neighbors_generator(source, n_neighbors):
            for i in range(n_neighbors):
                dist1 = np.linalg.norm(point1 - nn_points1[i])
                for j in range(n_neighbors):
                    dist2 = np.linalg.norm(point2 - nn_points2[j])
                    if compare_distances(dist1, dist2, distances_tolerance):

                        rot1_to_z, transl1_to_z = get_RT_in_z_direction(point1, nn_points1[i], dist1)
                        rot2_to_z, transl2_to_z = get_RT_in_z_direction(point2, nn_points2[j], dist2)

                        source_copy = copy.deepcopy(source)
                        target_copy = copy.deepcopy(target)
                        source_copy.paint_uniform_color([0, 0, 1])
                        target_copy.paint_uniform_color([1, 0, 1])

                        # point_cloud_viewer([target_copy, source_copy])

                        custom_roto_translate(target_copy, rot1_to_z, transl1_to_z)
                        custom_roto_translate(source_copy, rot2_to_z, transl2_to_z)

                        # point_cloud_viewer([target_copy, source_copy])

                        source_copy.paint_uniform_color([0, 0, 1])
                        target_copy.paint_uniform_color([1, 0, 1])
                        # o3d.visualization.draw_geometries([target_copy, source_copy])
                        icp = icp_search_arround_z(source_copy, target_copy, threshold, angle_step)
                        if icp is not None:
                            if icp.fitness > highest_fitness:
                                highest_fitness = icp.fitness
                                best_icp = icp
                        # o3d.visualization.draw_geometries([target_copy, source_copy])
    if best_icp is not None:
        return int(best_icp.fitness * n_points_source), n_points_source, n_points_target, best_icp.inlier_rmse, np.asarray(best_icp.correspondence_set)
    else:
        return 0, n_points_source, n_points_target, np.infty, []
