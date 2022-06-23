import pandas as pd
import numpy as np
import open3d as o3d
import random2
import os
import jv.folders as jvf
cfg = {
    "INPUT_PATH": "/mnt/datos/datasets/grapes_centers/",
}

# def baya_generator(x,y,z,r,n):
#     puntos_baya = []
#     for i in range(n):
#           random2.randint()
#         x_2 =

def cloud_generator(input_path, output_path):
    df = pd.read_csv(input_path)
    bayas = df['label'] == 'baya'
    df = df[bayas]

    df.drop(df.iloc[:, 0:4], axis=1, inplace=True)
    df.drop(df.iloc[:, 4:], axis=1, inplace=True)
    df = df.iloc[lambda x: x.index % 2 != 0]
    idx_ceros = df[df['Z'] == 0].index
    print(idx_ceros)
    df = df.drop(idx_ceros)

    video_names = df['img_name'].unique()

    for video_name in video_names:
        ply_path = f"{output_path}/{video_name[:19]}.ply"

        idx = df['img_name'] == video_name
        n_bayas = sum(idx)
        header = f"""ply
format ascii 1.0           
element vertex {n_bayas}
property double x           
property double y           
property double z           
end_header\n"""

        f = open(ply_path, 'w+')
        f.write(header)
        f.close()
        df_bayas = df[idx].drop('img_name', axis=1)
        df_bayas.to_csv(ply_path, index=False, mode="a", header=False, sep=' ')


if __name__ == "__main__":
    file_list = jvf.get_file_paths_list(cfg.get("INPUT_PATH"), pattern="*.csv")
    for file in file_list:
        working_directory, video_name = os.path.split(file)
        file_name_without_extension, extension = os.path.splitext(video_name)
        path = jvf.make_dir(working_directory, file_name_without_extension)
        cloud_generator(file, path)