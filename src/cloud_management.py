import open3d as o3d
import numpy as np
import copy

def get_minimum_distance(cloud):
    pc_tree = o3d.geometry.KDTreeFlann(cloud)
    points = np.asarray(cloud.points)
    min_distance = 100
    # points = np.append(points, [[0, 0, 0]], axis=0)
    for point in points:
        _, idx, _ = pc_tree.search_knn_vector_3d(point, 2)
        distance = np.linalg.norm(point - points[idx[1], :])
        if min_distance > distance:
            min_distance = distance
    return min_distance

def delete_points(cl, n_points):
    points = np.asarray(cl.points)
    idx = np.random.randint(0, len(points), n_points)
    print(f"Removed point index: {idx}")
    points = np.delete(points, idx, axis=0)
    cl.points = o3d.utility.Vector3dVector(points)


def add_noise_to_cloud(cl, std_dev):
    pts = np.asarray(cl.points)
    noise = np.random.normal(loc=0.0, scale=std_dev, size=pts.shape)
    pts = pts + noise
    cl.points = o3d.utility.Vector3dVector(pts)


def get_pairs(pc_points):
    pc_len = len(pc_points)
    for idx1 in range(pc_len):
        for idx2 in range(idx1 + 1, pc_len):
            yield pc_points[[idx1, idx2], :]

def conform_point_cloud(points):
    return o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))

def add_points(pc, points_to_add):
    """points_to_add np [[x1 y1 z1][x2 y2 z2]... ]"""
    points = np.asarray(pc.points)
    points = np.append(points, points_to_add, axis=0)
    return o3d.utility.Vector3dVector(points)

def extract_points(pc, center, n_points, type_flag):
    """type_flag: True return poincloud, False return np.array"""
    pc_tree = o3d.geometry.KDTreeFlann(pc)
    points = np.asarray(pc.points)
    # points = np.append(points, [[0, 0, 0]], axis=0)
    [k, idx, dist] = pc_tree.search_knn_vector_3d(center, n_points)
    sub_cloud_points = points[idx, :]
    if type_flag:
        sub_cloud = copy.deepcopy(pc)
        sub_cloud.points = o3d.utility.Vector3dVector(sub_cloud_points)
        return sub_cloud, idx
    else:
        return sub_cloud_points, idx