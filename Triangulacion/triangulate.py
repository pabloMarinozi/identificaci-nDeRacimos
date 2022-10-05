import subprocess
import os



# Directorio que contiene a todos los cuarteles a procesar
#input_dir = "../2022-02-17_Zuccardi_Piedra-Infinita_Volumetria/data_sources/fallidas_reintento"
input_dir = "/home/pablo/DHARMA/berry_tracking/output/VID_20220217_101324/mod4"
image_dir = "/home/pablo/DHARMA/berry_tracking/output/VID_20220217_101324"
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

cmd = "python3 Release/triangular_racimos_from_folder.py" \
                " -i " + input_dir + "/" + \
                " -m " + input_dir + "/" + \
                " -c data/" + calib_yaml + \
                " -s " + str(calib) + \
                " -v " + str(val_dist) + \
                " -o " + input_dir + "/" + \
                " --sufix " + path_vol
os.system(cmd)
