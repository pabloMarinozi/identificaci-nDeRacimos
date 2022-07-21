# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import argparse
import sys
from cvat_xml_parser import CVat_xml_Parser
from output_manager import OutputManager
from xml.dom import minidom


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description= """Procesa las annotations de volumetria y genera los bundles a partir del etiquetado.
        -i, --input_dir:  Directorio donde se encuentra el xml de cvat y los directorios con los pares de imágenes.
        -xml_left: Nombre del archivo xml de cvat de donde se extraeran las etiquetas del primer frame.
        -xml_right: Nombre del archivo xml de cvat de donde se extraeran las etiquetas del segundo frame.
        -ns_left: Estrategia de nombrado de archivos que se utilizó al etiquetar el xml izquierdo 
        -ns_right: Estrategia de nombrado de archivos que se utilizó al etiquetar el xml derecho 
        -ps_left: Estrategia de labels usadas al etiquetar el xml izquierdo (diferenciadas por captura como por ejemplo "Salentein")
        -ps_right: Estrategia de labels usadas al etiquetar el xml derecho (diferenciadas por captura como por ejemplo "Salentein")
        -o, --output_dir: Directorio dónde se almacenarán los archivos de salida
        """
    )
    parser.add_argument('-i','--input_dir', type=str, required=True)
    parser.add_argument('-xml_left', type=str, required=True)
    parser.add_argument('-xml_right', type=str, required=True)
    parser.add_argument('-ns_left', type=str, required=True)
    parser.add_argument('-ns_right', type=str, required=True)
    parser.add_argument('-ps_left', type=str, required=True)
    parser.add_argument('-ps_right', type=str, required=True)
    parser.add_argument('-o','--output_dir', type=str, required=True)
    args = parser.parse_args(args)


    base_dir = args.input_dir


    annotation = os.path.join(base_dir, args.xml_left)
    xmldoc = minidom.parse(annotation)
    naming_strategy = args.ns_left
    point_strategy = args.ps_left
    xml_parser = CVat_xml_Parser(xmldoc, naming_strategy, point_strategy)
    data_bundles_left = xml_parser.get_bundles()
    data_bundles_left["side"] = 0

    annotation = os.path.join(base_dir, args.xml_right)
    xmldoc = minidom.parse(annotation)
    naming_strategy = args.ns_right
    point_strategy = args.ps_right
    xml_parser = CVat_xml_Parser(xmldoc, naming_strategy, point_strategy)
    data_bundles_right = xml_parser.get_bundles()
    data_bundles_right["side"] = 1

    data_bundles = pd.concat([data_bundles_left,data_bundles_right])

    output_dir = args.output_dir
    output_manager = OutputManager(output_dir)
    df_tracks = output_manager.generate_df_tracks_csv(data_bundles)
    output_manager.generate_bundles_for_image(df_tracks)



if __name__ == "__main__":
    main()