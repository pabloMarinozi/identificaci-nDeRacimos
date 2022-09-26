from cmath import nan
import os
import argparse
import sys
import pandas as pd
import statistics
import math
import numpy
from pathlib import Path

def generate_triangulaciones(base_dir, camera_int, scale_dist, output_dir):
    for path in Path(base_dir).rglob('bundles.csv'):
        print("Triangulate:",path)
        os.system("export LD_LIBRARY_PATH=../Triangulacion/Release/lib/;export LD_LIBRARY_PATH=../Triangulacion/include/Thirdparty/g2o/lib;"+
         "../Triangulacion/Release/triangulacionDeBayas " + str(camera_int) + " " + str(path) + " " + str(path.parents[1]) + " " + str(scale_dist) + " " + str(path.parents[0]))
        # parameters /home/user/eclipse-workspace/Triangulacion/data/camaraCarlos1080.yaml /home/user/eclipse-workspace/Triangulacion/data/bundles/1388/bundles.csv 8.0

def agregar_resultados_en_csv(base_dir, val_dist, sufix):

    fulldf = None
    fullcsv_output_path = base_dir + "/keypoints_positions_" + sufix + ".csv"
    fullcsv_output_path_volumen = base_dir + "/volumenes_promedio_" + sufix + ".csv"

    csv_volumen=list()
    for path in Path(base_dir).rglob('Reproyecciones.csv'):
        print("Agregate:",path)
        df = pd.read_csv(path)


        racimo = os.path.dirname(path).split(sep="/")[-1]
        
        val_1 = float(nan)
        val_2 = float(nan)
        if df["d2val1"].notnull().values.any():
            val_1 = df[df["d2val1"].notnull()].iat[0,17]
        if df["d2val2"].notnull().values.any():      
            val_2 = df[df["d2val2"].notnull()].iat[0,18]
        val_dist = val_dist

        df_vol = df[df["label"]=="baya"]
        df_vol = df_vol[df_vol["r"]>0]
        df_vol = df_vol[df_vol["img_name"].str.contains("F0|F10")]
        #print("df_vol rows", df_vol.shape[0])
        if df_vol.empty == False:
            difx = df_vol["xrep"] - df_vol["x1cm"]
            dify = df_vol["yrep"] - df_vol["y1cm"]
            difx_2 = [ n ** 2 for n in difx]
            dify_2 = [ n ** 2 for n in dify]
            #print("difx",difx)
            #print("dify",dify)
            calibracion = [ math.sqrt(n) for n in [sum(x) for x in zip(difx_2,dify_2)] ]
            #print("calibracion:",calibracion)
            #print("radiosenpx:",df_vol["r"])
            radios = df_vol["r"] / calibracion
            #print("radios:",radios)
            volumenes = [ 4/3*math.pi*r**3 for r in radios ]
            #print(volumenes)
            volumen_promedio_sinnan = numpy.nanmean(volumenes)
            volumen_promedio_connan = numpy.mean(volumenes)
            nan_counts = numpy.count_nonzero(numpy.isnan(volumenes))
            no_nan_counts = numpy.count_nonzero(~numpy.isnan(volumenes))
        else:
            volumen_promedio_sinnan = float("nan")
            volumen_promedio_connan = float("nan")
            nan_counts = 0
            no_nan_counts = 0


        print("racimo:",racimo)
        print("volumen_promedio_sinnan:",volumen_promedio_sinnan)
        print("volumen_promedio_connan:",volumen_promedio_connan)
        print("cantidad_de_nans:", nan_counts)
        data={}
        data["racimo_id"]=racimo
        data["avg_vol"]=volumen_promedio_sinnan
        data["avg_vol_anynan"]=volumen_promedio_connan
        data["nan_counts"]=nan_counts
        data["no_nan_counts"]=no_nan_counts
        data["val_1"]=val_1
        data["val_2"]=val_2
        data["val_dist"]=val_dist
        csv_volumen.append(data)
        if fulldf is None:
            fulldf = df
        else:
            fulldf = pd.concat([fulldf,df])
    fulldf = pd.DataFrame(fulldf)
    fulldf.to_csv(fullcsv_output_path)
    csv = pd.DataFrame(csv_volumen)
    csv.to_csv(fullcsv_output_path_volumen)

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description= """Lee archivos csv con los bundles de keypoints
        -INPUT:
            --input_dir: Carpeta que contiene los csv con los bundles de los keypoints y las imagenes para realizar la reconstruccion.
            --camera_int: Archivo yaml que contienen los parametros intrinsicos de la camara.
            --scale_dist: Distancia en cm de los dos puntos de calibracion para dar escala a la nube 3d.
            --val_dist: Distancia en cm de los dos puntos de calibracion para dar escala a la nube 3d.
            --sufix: Sufijo de csv de salida
        -OUTPUT:
            Carpeta de salida, se almacenan los frames con los keypoints dibujados y un csv que contiene la informacion de todas las reconstrucciones.

        -EXAMPLE:
            python triangular_racimos_from_folder.py -i ./data/ -c ../data/camaraCarlos1080.yaml -s 8.0 -o ./output/
        """
    )
    parser.add_argument('-i','--input_dir', type=str, required=True)
    parser.add_argument('-m','--images_dir', type=str, required=True)
    parser.add_argument('-c','--camera_int', type=str, required=True)
    parser.add_argument('-s','--scale_dist', type=str, required=True)
    parser.add_argument('-v','--val_dist', type=str, required=True)
    parser.add_argument('-o','--output_dir', type=str, required=True)
    parser.add_argument('--sufix', type=str, required=True)
    args = parser.parse_args(args)
    final_outputdir= args.output_dir + args.sufix
    generate_triangulaciones(args.input_dir, args.camera_int, args.scale_dist, final_outputdir)
    agregar_resultados_en_csv(final_outputdir, args.val_dist, args.sufix)


if __name__ == "__main__":
    main()
