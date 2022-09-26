# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import argparse
import sys
from cvat_xml_parser import CVat_xml_Parser
from output_manager import OutputManager
from xml.dom import minidom
from output_manager import Output_Strategy

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description= """Procesa las annotations de volumetria y genera los bundles a partir del etiquetado.
        -i, --input_dir:  Directorio donde se encuentra el xml de cvat y los directorios con los pares de imágenes.
        -xml: Nombre del archivo xml de cvat. Por defecto es "annottations.xml"
        -ns: Estrategia de nombrado de archivos que se utilizó al etiquetar (mauro-videos o fernanda-videos)
        -ps: Estrategia de labels usadas al etiquetar (diferenciadas por captura como por ejemplo "Salentein")
        -o, --output_dir: Directorio dónde se almacenarán los archivos de salida
        Example:
            python main.py -i ./data/ -ns 0_1 -ps fecovita -o ./output
        """
    )
    parser.add_argument('-i','--input_dir', type=str, required=True)
    parser.add_argument('-xml', type=str)
    parser.add_argument('-ns', type=str, required=True)
    parser.add_argument('-ps', type=str, required=True)
    parser.add_argument('-o','--output_dir', type=str, required=True)
    args = parser.parse_args(args)


    base_dir = args.input_dir
    if args.xml is None:
        annotation = os.path.join(base_dir, "annotations.xml")
    else:
    	annotation = os.path.join(base_dir, args.xml)
    xmldoc = minidom.parse(annotation)

    naming_strategy = args.ns
    point_strategy = args.ps
    xml_parser = CVat_xml_Parser(xmldoc, naming_strategy, point_strategy)
    data_bundles = xml_parser.get_bundles()

    print(data_bundles.shape)

    output_dir = args.output_dir
    output_manager = Output_Strategy.get_output_manager(output_dir, point_strategy)
    df_tracks = output_manager.generate_df_tracks_csv(data_bundles)
    output_manager.generate_bundles_for_image(df_tracks)



if __name__ == "__main__":
    main()

