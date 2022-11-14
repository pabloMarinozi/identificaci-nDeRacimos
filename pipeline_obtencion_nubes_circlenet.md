# Pipeline de identificación automática DeRacimos

0. Subir los videos a un drive para que puedan ser pasados como entrada al notebook [berry_tracking.ipynb](https://colab.research.google.com/drive/190oIcmfRJJuopcApVaGFiqxiQDR9Utjk?usp=sharing) 

1. Ejecutar el notebook [berry_tracking.ipynb](https://colab.research.google.com/drive/190oIcmfRJJuopcApVaGFiqxiQDR9Utjk?usp=sharing) y descargar el archivo output.zip

2. Ejecutar el notebook nubes_circlenet.Rmd que recibe los detections.csv que generó berry_tracking y genera los bundles.csv que necesita la triangulación.

La salida es un archivo bundles.csv en cada carpeta de racimo/video que contiene las coordenadas 2d de las bayas en varias imágenes para poder hacer una reconstrucción

3. Correr el script triangulate.py de Triangulacion que genera los csv con la posición 3D de cada baya y punto etiquetado en cvat. Los argumentos deben escribirse dentro del script. 

* La variable input_dir es la ruta al directorio que contiene las carpetas para cada racimo/video (la carpeta mod que contiene al bundles.csv)
* La variable image_dir es la ruta al directorio que contiene las imagenes donde se va a dibujar la reproyeccion
* La variable calib está en centímetros y es la distancia entre los puntos de calibración (se ignora)
* La variable val_dist está en centímetros y es la distancia entre los puntos de validación (se ignora)
* La variable path_vol es el nombre de la carpeta que se creará en input_dir para guardar las salidas

Las salidas son:
* keypoints_positions_volume.csv que contiene toda la info 3D de todas las nubes trianguladas en esa corrida
* una carpeta por racimo que contiene: un csv (Reproyecciones.csv) con la misma info 3D pero solo de ese racimo y los frames con las reproyecciones dibujadas para evaluar a ojo la calidad de las reconstrucciones

4. Correr el script  clouds_from_individual_grapes_centers.py en la carpeta cloud_generator. Este genera los archivos .ply de cada nube a partir de la info almacenada en Reproyecciones.csv

* --csv-name: nombre del archivo csv con la info de las reconstrucciones
* --base-dir: carpeta que contiene todos los archivos cuyo nombre sea csv-name
* --output_dir: Carpeta de salida, se almacenan los .ply de las nubes del csv

5. Correr el script labeler.py que genera el archivo labels.csv que contiene los ground truth de la identiicación (nubes que surgieron del mismo racimo tienen la misma etiqueta)

6. Correr el script main_nubes_circlenet.py que ejecuta icp con alineacion y cambio de escala y genera los archivos nubes_circlenet{radio}.csv

7. Generar las métricas y gráficos en R a partir de los archivos anteriores. Los notebooks se encuentran en identificaci-nDeRacimos/output/notebooksMetricas
