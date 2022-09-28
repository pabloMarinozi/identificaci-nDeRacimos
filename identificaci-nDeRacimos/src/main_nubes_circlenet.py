from icp_with_alignment import icp_scaled_and_aligned
from cloud_management import add_noise_to_cloud, get_minimum_distance
import copy
import random
import sys
import argparse
import open3d as o3d
import numpy as np
import pandas as pd
from time import time


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description= """Etiqueta nubes 3D a partir de su nombre
        -INPUT:
            --input_dir: folder with inputs
        -OUTPUT:
            --output_dir: Carpeta de salida dondese creará el archivo labels
        """
    )
    parser.add_argument('-i','--input_dir', type=str, required=True)
    parser.add_argument('-o','--output_dir', type=str, required=True)
    args = parser.parse_args(args)

    inputs_path = args.input_dir+"/labels.csv"
    inputs_df = pd.read_csv(inputs_path)
    n_clouds = len(inputs_df.index)
    clouds = {} #dict containing point clouds
    for name in inputs_df["cloud_name"]:
        cloud = o3d.io.read_point_cloud(args.input_dir+name)
        clouds[name] = cloud


    #realiza el producto cartesiano entre las nubes
    df = inputs_df.merge(inputs_df, how='cross')
    #print(df.colnames())
    #df.to_csv(args.input_dir+"/df.csv")
    cloud_names_1 = df["cloud_name_x"].tolist()
    cloud_names_2 = df["cloud_name_y"].tolist()
    labels_1 = df["label_x"].tolist()  
    labels_2 = df["label_y"].tolist()

    ##### hiper-parámetros ####
    n_neighbors = 1             # cantidad de vecinos por cada punto de una nube con los que va a intentar alinear
    distances_tolerance = 0.2   # Solo comparará puntos que en ambas nubes estén a distancias similares ) +/- 20%
    threshold_percentage_list = [0.1,0.2,0.3,0.4,0.5,1]  # porcentaje de la distancia mínima en la nube a usar como trheshold
    angle_step_list = [1/4]     # paso de rotación de la nube "source" alrededor del eje z

    n = 0
    #times = np.zeros((n_clouds, n_clouds), dtype=float)
    start_time = time()
    rows = [] 
    for thresh in threshold_percentage_list:
        for step in angle_step_list: 
            for i, cn1 in enumerate(cloud_names_1):
                cn2 = cloud_names_2[i]
                source = clouds[cn1]
                target = clouds[cn2]
                label = labels_1[i]==labels_2[i]
                minimun_distance = get_minimum_distance(source) # lo hice sobre source porque es la que rota sobre z

                start = time()
                angle = np.pi * step
                metric = icp_scaled_and_aligned(source, target, thresh,
                                             n_neighbors, angle)
                giros = 2/step
                row = pd.DataFrame(
                    [[cn1,metric[1],cn2,metric[2],metric[0],label,metric[3],thresh,giros]],
                 columns=["nube1","tamaño_nube1","nube2","tamaño_nube2","matcheos","label","rmse","radio","giros"])
                # Devuelve: (cantidad de matcheos, cantidad de puntos nube source, cantidad de puntos nube target, rmse, conjunto de correspondencia)
                rows.append(row)
                #end = time()
                #times[i, j] = end - start
                print(i, len(cloud_names_1), metric[0])                    
        data = pd.concat(rows, axis=0)
        path = args.output_dir + "/nubes_circlenet"+str(thresh)+".csv"
        data.to_csv(path)
    end_time = time()
    print(times)
    print(end_time - start_time)
    

if __name__ == "__main__":
    main()
    