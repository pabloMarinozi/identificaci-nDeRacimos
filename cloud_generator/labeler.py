import sys
import argparse
import os
import pandas as pd
from pathlib import Path

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
    ply_names = []
    video_names_list = []
    video_names_set = set()
    for path in Path(args.input_dir).rglob('*.ply'):
        working_directory, name = os.path.split(path)
        ply_names.append(name)
        name_list = name.split("_mod")
        video_names_list.append(name_list[0])
        video_names_set.add(name_list[0])
    labels = []
    for name in video_names_list:
        for i, name2 in enumerate(video_names_set):
            if name == name2:
                labels.append(i)
                break
    pd.DataFrame(
        list(zip(ply_names, labels)),
            columns =['cloud_name', 'label']).to_csv(args.output_dir+"/labels.csv",index=False)

    


    


if __name__ == "__main__":
    main()