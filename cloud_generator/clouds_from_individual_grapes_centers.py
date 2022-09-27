import argparse
import pandas as pd
import numpy as np
import open3d as o3d
#import random2
import sys
import os
from glob import glob
from pathlib import Path

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


    #lee puntos 3D
    df = pd.read_csv(input_path)
    bayas = df['label'] == 'baya'
    df = df[bayas]
    df = df[["track_id","X","Y","Z"]].drop_duplicates()
    df.to_csv(output_path+".csv", index=False)
    
    #filtra puntos defectuosos
    idx_ceros = df[df['Z'] == 0].index
    #~print(idx_ceros)
    df = df.drop(idx_ceros)

    #guarda ply
    n_bayas = len(df.index)
    header = f"""ply
    format ascii 1.0           
    element vertex {n_bayas}
    property double x           
    property double y           
    property double z           
    end_header\n"""
    ply_path = output_path+".ply"
    f = open(ply_path, 'w+')
    f.write(header)
    f.close()
    df_bayas = df.drop('track_id', axis=1)
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
            --base_dir: folder with inputs
            --csv_name: name of csv files to process
        -OUTPUT:
            --output_dir: Carpeta de salida, se almacenan los .ply de las nubes del csv
        """
    )
    parser.add_argument('-b','--base_dir', type=str, required=True)
    parser.add_argument('-c','--csv_name', type=str, required=True)
    parser.add_argument('-o','--output_dir', type=str, required=True)
    args = parser.parse_args(args)
    file = args.csv_name
    dir1, dir2 = os.path.split(args.output_dir)
    output_path = make_dir(dir1, dir2)
    for path in Path(args.base_dir).rglob(file):
        #print(path)
        working_directory, _ = os.path.split(path)
        parent, frames = os.path.split(working_directory)
        parent, mod = os.path.split(parent)
        _, video_name = os.path.split(parent)
        output_name = video_name +"_"+ mod + "_" + frames
        ply_generator(path, output_path+"/"+output_name)
    
    

if __name__ == "__main__":
    main()
        
