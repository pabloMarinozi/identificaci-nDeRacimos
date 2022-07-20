import argparse
import pandas as pd
import numpy as np
import open3d as o3d
import random2
import sys
import os
from glob import glob

def make_dir(path, name):
    """
    check if exist a "name" directory inside the "path". If doesn't, it created
    inputs:
        path: string containing the path to create the directory
        name: string containing the name of the directory
    return:
        string containing the directory path
    """
    new_dir_name = path + '/' + name
    if not os.path.isdir(new_dir_name):
        os.mkdir(new_dir_name)
    return new_dir_name


def get_file_paths_list(path_to_search, pattern="*.mp4"):
    """
    return a list of paths to all the files with extension given by the "pattern" inside the "path_to_search"
    inputs:
        path_to_search: string containing the path to the directory in which to search for the pattern
        pattern: a string containing the extension of the files being searched for
    """
    files = []
    for dir, _, _ in os.walk(path_to_search):
        print(glob(os.path.join(dir, pattern)))
        files.extend(glob(os.path.join(dir, pattern)))
    l = len(files)
    if l == 0:
        raise Exception(f"El directorio {path_to_search} no existe o no contiene archivos {pattern}")
    return files



def ply_generator(input_path, output_path):
    """
    generate a ply file from a csv generated with the óptima pipeline getting the center of grapes
    from the manual labeling of 3 points of grapes in a set of images obtained from a vide of a bunch
    inputs:
        input_path: srting containing the path to the csv file
        output_file: string containing the path in which the ply is going to be saved
    """
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



"""
script that generates ply files from the all csv found inside the  INPUT_PATH
It generates a folder for each csv file, and inside that folder save all the ply files, each 
named with the video file that generate it.
"""

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description= """Genera nubes ply a partir de la info 3D del csv
        -INPUT:
            --input_csv: path to input csv
        -OUTPUT:
            --output_dir: Carpeta de salida, se almacenan los .ply de las nubes del csv
        """
    )
    parser.add_argument('-i','--input_csv', type=str, required=True)
    parser.add_argument('-o','--output_dir', type=str, required=True)
    args = parser.parse_args(args)
    file = args.input_csv
    working_directory, video_name = os.path.split(file)
    file_name_without_extension, extension = os.path.splitext(video_name)
    path = make_dir(args.output_dir, file_name_without_extension)
    ply_generator(file, path)

if __name__ == "__main__":
    main()
        
