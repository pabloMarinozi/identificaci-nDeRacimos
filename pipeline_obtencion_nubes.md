# identificación DeRacimos

La salida de CVAT es un annotations.xml

annotations.xml -> winter-variables/code/peso-de-racimo/bundles_vol_from_vol_annotations_Fecovita.py -> bundles.csv

bundles.csv contiene las coordenadas 2d de las bayas en ambas imágenes

bundles.csv -> winter-variables/code/Triangulacion/Debug/ triangular_racimos_from_folder.py -> keypoints_positions_volume.csv

keypoints_positions_volume.csv contiene la info 3D de muchas nubes separadas por nombre del video

keypoints_positions_volume.csv -> identificaci-nDeRacimos/src/clouds_from_grapes_centers.py -> video_name.ply 

video_name.ply -> identificaci-nDeRacimos/src/main...  -> csv con resultados de icp (matcheos y rsme)

csv con resultados de icp (matcheos y rsme) -> notebooks de R -> grafiquitos
