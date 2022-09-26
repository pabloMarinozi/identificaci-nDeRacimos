from pathlib import Path
import pandas as pd

base_dir="/home/pablo/DHARMA/identificaci-nDeRacimos/2022-02-17_Zuccardi_Piedra-Infinita_Volumetria/data_sources/train_0_1"
with open('01_etiquetas.txt', 'w') as f:
	for path in Path(base_dir).rglob('bundles.csv'):
		f.write(str(path))
		f.write("\n")
with open('01_reconstruccion.txt', 'w') as f:
	for path in Path(base_dir).rglob('Reproyecciones.csv'):
		f.write(str(path))
		f.write("\n")
