from icp_with_alignment import icp_scaled_and_aligned
import sys
import argparse
import open3d as o3d
import numpy as np
from time import time
import pandas as pd

def get_points_ids(dir, name):
    df = pd.read_csv(dir + name[:-3] +'csv')
    idx_ceros = df[df['Z'] == 0].index
    df = df.drop(idx_ceros)
    return list(df['track_id'])


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    dirs = ['thresh0.6/', 'thresh0.7/', 'thresh0.8/', 'thresh0.9/' ]
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description= """Etiqueta nubes 3D a partir de su nombre
        -INPUT:
            --input_dir: folder with inputs
        -OUTPUT:
            --output_dir: Carpeta de salida donde se creará el archivo labels
        """
    )
    parser.add_argument('-i', '--input_dir', type=str, required=True)
    parser.add_argument('-o', '--output_dir', type=str, required=True)
    args = parser.parse_args(args)
    for dir in dirs:
        inputs_path = args.input_dir+dir+"/labels.csv"
        inputs_df = pd.read_csv(inputs_path)
        n_clouds = len(inputs_df.index)
        clouds = {} #dict containing point clouds
        cloud_idx = 0
    ####
        for name, label in zip(inputs_df["cloud_name"], inputs_df["label"]):
            cloud = o3d.io.read_point_cloud(args.input_dir+dir + name)
            points_ids = get_points_ids(args.input_dir+dir, name)
            clouds[cloud_idx] = [name, cloud, label, points_ids]
            cloud_idx += 1
    ####


        ##### hiper-parámetros ####
        n_neighbors = 1             # cantidad de vecinos por cada punto de una nube con los que va a intentar alinear
        distances_tolerance = 0.2   # Solo comparará puntos que en ambas nubes estén a distancias similares ) +/- 20%
        threshold_percentage_list = [ 0.02, 0.025, 0.03]  # porcentaje de la distancia en la nube a usar como trheshold
        angle_step_list = [1/4]     # paso de rotación de la nube "source" alrededor del eje z

        start_time = time()
        n_clouds = len(clouds)
        for i, thresh in enumerate(threshold_percentage_list):
            print(f"thresh: {thresh} ; iter {i+1} de {len(threshold_percentage_list)}")
            for step in angle_step_list:
                result = np.empty((int(((n_clouds ** 2) / 2) + n_clouds/2), 10), dtype=object) #
                counter = 0
                stime = time()
                for i in range(len(clouds)):
                    for j in range(i, len(clouds)):
                        cn1 = clouds[i][0]
                        cn2 = clouds[j][0]
                        label_1 = clouds[i][2]
                        label_2 = clouds[j][2]
                        overlap = 0
                        source = clouds[i][1]
                        target = clouds[j][1]
                        label = cn1[:2] == cn2[0:2]
                        start = time()
                        angle = np.pi * step
                        metric = icp_scaled_and_aligned(source, target, thresh,
                                                        n_neighbors, angle, distance_criterion='target')
                        giros = 2 / step
                        result[counter, :] = cn1, metric[1], cn2, metric[2], metric[0], overlap, label, metric[3], thresh, giros

                        # Devuelve: (cantidad de matcheos, cantidad de puntos nube source, cantidad de puntos nube target, rmse, conjunto de correspondencia)

                        print(cn1+f' (n:{metric[1]})', cn2 + f' ({metric[2]})')
                        print(f"counter: {counter+1}/{int(((len(clouds)**2)/2)+len(clouds)/2)}, matcheos: {metric[0]}, overlap: {overlap}") #
                        counter += 1
                frame = pd.DataFrame(result, columns=["nube1", "tamaño_nube1", "nube2", "tamaño_nube2", "matcheos", "overlap", "label", "rmse", "radio", "giros"])
                path = args.output_dir + dir + "/N_thresh_0.6_radio_"+str(thresh)+".csv"
                frame.to_csv(path)
                bucle_time = time()
                print(bucle_time - start_time)


    

if __name__ == "__main__":
    main()
