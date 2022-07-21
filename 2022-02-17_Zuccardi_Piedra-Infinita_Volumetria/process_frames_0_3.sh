#!/bin/bash

function help {
	   echo ""
	   echo ""
	   echo "USAGE: ./process_frames.sh --input (-i) input-folder --output (-o) output-folder -l -d"
	   echo ""
	   echo "   Tomas los pares de frames extraídos en un directorio dado y los procesa: crea una carpeta para cada par de frames (formato requerido para scripts de QRs) y si se indica la opción -l (--landscape) se rotan todas las imágenes para que queden con orientación horizontal."
	   echo ""
	   echo "    --input     (-i)  Path a la carpeta que contiene los videos a los que se les extraerá los frames."
	   echo "    --output    (-o)  Path a la carpeta donde se ubicarán los frames extraídos. De no indicarse uno será en la misma carpeta de entrada."
	   echo "    --landscape (-l)  Si se especifica, las imágenes que se encuentren con orientación vertical son rotadas 90 grados en sentido contrario a las agujas del reloj."
	   echo "    --help (-h)  Muestra la ayuda."
	   echo ""
	   echo ""
   	   
	   
}

# Initial values
debug="FALSE"
landscape="NULL"
input_folder="NULL"
output_folder="NULL"

until [ -z $1 ] ; do
	flag=$1
	
	[[ $flag = "-i" || $flag = "--input" ]] && input_folder="$2" && shift
	[[ $flag = "-o" || $flag = "--output" ]] && output_folder="$2" && shift
	[[ $flag = "-l" || $flag = "--landscape" ]] && landscape="TRUE"
	[[ $flag = "-d" || $flag = "--debug" ]] && debug="TRUE"
	[[ $flag = "-h" || $flag = "--help" ]] && help && exit 0
	shift 
done


[[ $output_folder = "NULL" ]] && output_folder=$input_folder

input_folder=${input_folder%/}
input_folder=${input_folder#/}
output_folder=${output_folder%/}
output_folder=${output_folder#/}


# We remove the leading dot in extension (if exist)
extention="*F0.png"

[[ $debug = "TRUE" ]] && echo "input_folder: $input_folder"
[[ $debug = "TRUE" ]] && echo "landscape: $landscape"
[[ $debug = "TRUE" ]] && echo "extention: $extention"


for FILE in $(ls $input_folder/$extention); do 
	left_img=$FILE
	right_img=${left_img/'_F0.png'/'_F3.png'}
	base_name=${left_img##*/} 
	
	out_path=${base_name/'_F0.png'/''}
	out_path=$output_folder/$out_path/

	[[ $debug = "TRUE" ]] && echo "---------------------------------"
	[[ $debug = "TRUE" ]] && echo "left_img:  $left_img"
	[[ $debug = "TRUE" ]] && echo "right_img: $right_img"
	[[ $debug = "TRUE" ]] && echo "out_path:   $out_path"

    if [ $landscape = "TRUE" ]; then
		w=`identify -format '%w' $left_img`
		h=`identify -format '%h' $left_img`
		if (( w < h )); then
			echo "Rotated: $left_img"
			convert $left_img -rotate -90 $left_img
		fi

		w=`identify -format '%w' $right_img`
		h=`identify -format '%h' $right_img`
		if (( w < h )); then
			echo "Rotated: $right_img"
			convert $right_img -rotate -90 $right_img
		fi
    fi

    mkdir -p $out_path
    mv $left_img $out_path/
    mv $right_img $out_path/
	
done
