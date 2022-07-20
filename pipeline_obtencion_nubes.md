# Pipeline de identificación DeRacimos

0. Descargar las imágenes izquierda y derecha del server DHARMa, ponerlas todas en una carpeta y ejecutar process_frames.sh. Esto producirá como salida una carpeta para cada racimo/video con los dos frames que se etiquetaron. (NOTA: process_frames.sh requiere tener instalado imagemagick para poder rotar las imagenes verticales sudo apt install imagemagick-6.q16)

1. Descargar de CVAT el xml con las etiquetas y ponerlo en la carpeta donde están las carpetas de los racimos/videos

2. Correr el main.py de bundles_vol_from_vol_annotations. Tener cuidado de elegir la naming_strategy que corresponda con el sufijo de las imágenes izquierda y derecha a usar. También debe elegir la point_parsing_strategy correspondiente con el estilo de etiquetado usado en el proyecto. Actualmente la única strategy programada es la que se usó para la captura fecovita (con 3 puntos a la izquierda, uno a la derecha y sin qrs) 

Ejemplo de llamada: python3 main.py -i ../2022-02-17_Zuccardi_Piedra-Infinita_Volumetria/data_sources/train_0_3/ -xml annotations_bonarda_frame3_hasta31.xml -ns 0_3 -ps fecovita -o../2022-02-17_Zuccardi_Piedra-Infinita_Volumetria/data_sources/train_0_3/ 

La salida es un archivo bundles.csv en cada carpeta de racimo/video que contiene las coordenadas 2d de las bayas en ambas imágenes para poder hacer una reconstrucción

3. Correr el script triangulate.py de Triangulacion que genera los csv con la posición 3D de cada baya y punto etiquetado en cvat. Los argumentos deben escribirse dentro del script. 

* La variable input_dir es la ruta al directorio que contiene las carpetas para cada racimo/video (el mismo input_dir del paso2)
* La variable calib está en centímetros y es la distancia entre los puntos de calibración
* La variable val_dist está en centímetros y es la distancia entre los puntos de validación
* La variable path_vol es el nombre de la carpeta que se creará en input_dir para guardar las salidas

Las salidas son:
* keypoints_positions_volume.csv que contiene toda la info 3D de todas las nubes trianguladas en esa corrida
* una carpeta por racimo que contiene: un csv con la misma info 3D pero solo de ese racimo, los frames con las reproyecciones dibujadas para evaluar a ojo la calidad de las reconstrucciones

4. Correr el script  clouds_from_grapes_centers.py en la carpeta identificaci-nDeRacimos. Este genera los archivos .ply de cada nube a partir de la info almacenada en keypoints_positions_volume.csv

* --input_csv: path to input csv
* --output_dir: Carpeta de salida, se almacenan los .ply de las nubes del csv



keypoints_positions_volume.csv -> identificaci-nDeRacimos/src/clouds_from_grapes_centers.py -> video_name.ply 

6. video_name.ply -> identificaci-nDeRacimos/src/main...  -> csv con resultados de icp (matcheos y rsme)

7. csv con resultados de icp (matcheos y rsme) -> notebooks de R -> grafiquitos
