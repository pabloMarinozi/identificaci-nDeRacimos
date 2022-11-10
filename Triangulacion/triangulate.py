import subprocess
import os
import cv2


# Directorio que contiene a todos los cuarteles a procesar
# input_dir = "../2022-02-17_Zuccardi_Piedra-Infinita_Volumetria/data_sources/fallidas_reintento"
input_dir = "/home/valen/input_bundles_from_detections/VID_20220217_153655/mod4"
image_dir = "/home/valen/input_bundles_from_detections/VID_20220217_153655"
# Extesión de las imágenes a procesar (sin el punto)
ext_img = "png"
# Calibración usada durante la reconstrucción 3D y estimación de volúmenes
calib = 2
# Distancia entre los puntos de validación
val_dist = 2
# Nombre del directorio de salida para la info de los volúmenes de cada cuartel
path_vol = "volumes"
# imagen
img = cv2.imread(image_dir, cv2.IMREAD_UNCHANGED)
alto = img.shape[0]
ancho = img.shape[1]
print("\n\n")
print("#"*80)
print("\n>>> COMPUTE VOLUMES FROM BUNDLES")

if alto < ancho:
    calib_yaml = "camaraMaurosalentein.yaml"
else:
    calib_yaml = "camaraMaurosalenteinVertical.yaml"

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
