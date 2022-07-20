import open3d as o3d
import numpy as np
import copy

def get_minimum_distance(cloud):
    """
    compute the distance between all the pairs of grapes and return the minimun
    distance
    input:
        cloud: PointCloud object (open3d)
    return:
        min_distance: minimun distance (float)
    """
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
    """
    delete n_points from the PointCloud cl
    inputs:
        cl: PointCloud object (open3d)
        n_points: number of points to delete from cl
    """
    points = np.asarray(cl.points)
    idx = np.random.randint(0, len(points), n_points)
    print(f"Removed point index: {idx}")
    points = np.delete(points, idx, axis=0)
    cl.points = o3d.utility.Vector3dVector(points)


def add_noise_to_cloud(cl, std_dev):
    """
    add gaussian noise to a point cloud
    inputs:
        cl: PoinCloud object (open3d)
        std_dev: standard deviation of the gaussian noise to add
    """
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
    """
    create a PointCloud object from a matrix
    inputs:
        points: a mumpy matrix with shape (n, 3) (n arbitrary points and x, y, z coordinates)
    return:
        PointCloud object (open3d)
    """
    return o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))

def add_points(pc, points_to_add):
    """
    add points to a point cloud
    inputs:
        pc: PointCloud object
        points_to_add: numpy matrix with shape (n, 3)  [[x1 y1 z1][x2 y2 z2]... ]
    return:
        original PointCloud object containing the new points
    """
    points = np.asarray(pc.points)
    points = np.append(points, points_to_add, axis=0)
    return o3d.utility.Vector3dVector(points)

