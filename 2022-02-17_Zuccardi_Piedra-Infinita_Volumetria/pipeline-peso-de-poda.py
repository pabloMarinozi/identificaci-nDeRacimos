import subprocess
import os


# ETAPAS DEL PIPELINE PARA IDENTIFICACIÓN DE RACIMOS: True vuelve a ejecutar la etapa y
# pisa la info existente. False no lo ejecuta pero se asume que la etapa que sigue ya
# cuenta con la info necesaria.
do_bundles_from_cvat = False
do_reconstruction = True

# Directorio que contiene a todos los cuarteles a procesar
input_dir = "./data_sources/train_0_3"
# Extesión de las imágenes a procesar (sin el punto)
ext_img = "png"
# Calibración usada durante la reconstruccion 3D y estimación de volúmenes
calib = 2
# Distancia entre los puntos de validación
val_dist = 2
# Nombre del directorio de salida para la info de los volumenes de  cada cuartel
path_vol = "volumes"

print("\n\n")
print("#"*80)
print("\n>>> COMPUTE VOLUMES FROM BUNDLES")

calib_yaml = "camaraMaurosalentein.yaml"

path_temp = os.path.join(input_dir, "volumes/")
if not os.path.exists(path_temp):
    # Create a new directory because it does not exist
    os.makedirs(path_temp)

cmd = "python3 ../Triangulacion/Debug/triangular_racimos_from_folder.py" \
                " -i " + input_dir + "/" + \
                " -c ../Triangulacion/data/" + calib_yaml + \
                " -s " + str(calib) + \
                " -v " + str(val_dist) + \
                " -o " + input_dir + "/" + \
                " --sufix " + path_vol
os.system(cmd)
