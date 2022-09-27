//============================================================================
// Name        : InputReader.cpp
// Author      : Pablo
// Version     :
// Copyright   : Hecho para Óptima.
// Description : Escribe las salidas al algoritmo
//============================================================================

#include <opencv2/core/mat.hpp>
#include <opencv2/core/types.hpp>
#include <opencv2/imgcodecs.hpp>
#include <OutputWriter.h>
#include <dirent.h>
#include <stddef.h>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>

using namespace std;

OutputWriter::OutputWriter(string strOutputPath, string strMatchesPath,int f0, int f1 ){
	string directory = "/"+to_string(f0)+"_"+to_string(f1);
	/*
	const size_t last_slash_idx = strMatchesPath.find_last_of('/');
	if (std::string::npos != last_slash_idx)
	{
	    directory = strMatchesPath.substr(0, last_slash_idx);
	}
	const size_t last_slash_idx2 = directory.find_last_of('/');
	directory = directory.substr(last_slash_idx2);
	cout<<"directory: "<< directory<<endl;
	directory = directory+to_string(f0)+"_"+to_string(f1);*/


	//char* ruta = "";
	//sprintf(ruta, "%s", strOutputPath.c_str());
	DIR *dirp = opendir(strOutputPath.c_str());
	if (dirp == NULL) {
		char* comando = new char[510];

		sprintf(comando, "mkdir %s", strOutputPath.c_str());
		std::system(comando);
		cout << "Se ha creado el directorio de salida en la ruta " << strOutputPath
				<< endl;
	} else {
		cout << "Ya existia el directorio de salida en la ruta " << strOutputPath
				<< endl;
	}
	//sprintf(ruta, "%s%s", strOutputPath.c_str(),directory.c_str());
	strOutputPath = strOutputPath+directory;
	DIR *dirp2 = opendir(strOutputPath.c_str());
	if (dirp2 == NULL) {
		char* comando = new char[510];

		sprintf(comando, "mkdir %s", strOutputPath.c_str());
		std::system(comando);
		cout << "Se ha creado el directorio de salida en la ruta " << strOutputPath
				<< endl;
	} else {
		cout << "Ya existia el directorio de salida en la ruta " << strOutputPath
				<< endl;
	}
	this->strOutputPath = strOutputPath;
}

void OutputWriter::guardarImagenes(map<int, cv::Mat> imgs, map<int, string> names){
	for (auto const& [key, val] : imgs){
		char* nombre;
		cv::Mat img = val;
		sprintf(nombre, "%s/%s", strOutputPath, names[key]);
		const string ruta = strOutputPath+"/"+to_string(key)+".png";
		cv::imwrite(ruta,img);
	}
}

void OutputWriter::guardarResultados(vector<long unsigned int> allKfIds,
		map<int, vector<float> > errors_map,
		map<int, vector<cv::Point2f> > rep_map,
		map<int, vector<cv::Point2f> > kps_map,
		map<int, vector<cv::Point2f> > points_map,
		map<int, vector<int> > track_id_map,
		map<int, cv::Point3d> mps,
		int cal_1, int cal_2, map<int, string> names,
		map<int, vector<float> > radios,
		map<int, vector<float> > vols_rep_map,
		map<int, vector<float> > vols_real_map,
		map<int, string> labels) {
	ofstream myfile;
	myfile.open(strOutputPath+"/Reproyecciones.csv");
	if (myfile.is_open()) {

		//Escribe encabezados
		myfile << "track_id,frame_id,label,X,Y,Z,img_name,x,y,r,vol_real,vol_rep,xrep,yrep,error,x1cm,y1cm,d2val1,d2val2";
		myfile << endl;

		//Encuentra las coordenadas x,y,z de val_1 y val_2
		cv::Point3d val1_3d;
		cv::Point3d val2_3d;
		for(std::map<int,cv::Point3d>::iterator iter = mps.begin(); iter != mps.end(); ++iter)
		{
			//columna "track_id"
			int track_id =  iter->first;
			//columnas "x","y" y "z"
			cv::Point3d p = iter->second;

			if(labels[track_id] == "val_1"){
				val1_3d=p;
			}

			if(labels[track_id] == "val_2"){
				val2_3d=p;
			}

		}

		//Itera sobre los mappoints y frames para generar una fila para cada uno
		for(std::map<int,cv::Point3d>::iterator iter = mps.begin(); iter != mps.end(); ++iter)
		{
			//columna "track_id"
			int track_id =  iter->first;
			//columnas "x","y" y "z"
			cv::Point3d p = iter->second;

			//columnas por frame
			for (auto frame_index : allKfIds){

				myfile << track_id <<","<< frame_index <<","<< labels[track_id];

				myfile << ","<<p.x<< ","<<p.y<< ","<<p.z;

				//verifica si el map point es visible en el frame
				vector<int> tracks_del_frame = track_id_map[frame_index];
				int index_del_track_en_el_frame = -1;
				for (int kp_index = 0; kp_index < tracks_del_frame.size(); ++kp_index){
					if(tracks_del_frame[kp_index] == track_id)
						index_del_track_en_el_frame =  kp_index;
				}

				//si es visible...
				if(index_del_track_en_el_frame>-1){
					//columna "img_name_"
					myfile << ","<< names[frame_index];
					//columnas "x_" e "y_"
					cv::Point2f observacion = kps_map[frame_index][index_del_track_en_el_frame];
					myfile << ","<<observacion.x<< ","<<observacion.y;
					//columna "r_"
					myfile << ","<< radios[frame_index][index_del_track_en_el_frame];
					//columnas "vol_real_" y "vol_rep_"
					myfile << ","
							<< vols_real_map[frame_index][index_del_track_en_el_frame]
							<< ","
							<< vols_rep_map[frame_index][index_del_track_en_el_frame];
					//columnas "x_rep_" e "y_rep_"
					cv::Point2f reproyeccion = rep_map[frame_index][index_del_track_en_el_frame];
					myfile << ","<<reproyeccion.x<< ","<<reproyeccion.y;
					//columna "error_"
					myfile << ","<< errors_map[frame_index][index_del_track_en_el_frame];
					//columnas "x_1cm_" e "y_1cm_"
					cv::Point2f point1cm = points_map[frame_index][index_del_track_en_el_frame];
					myfile << ","<<point1cm.x<< ","<<point1cm.y;

					//Distancia a val1
					if(labels[track_id] == "val_1"){
						float d2val1 = cv::norm(val1_3d - p);
						if(d2val1 != 0){
							myfile << "," << d2val1;
						}else{
							myfile << ",NULL";
						}
					}else{
						myfile << ",NULL";
					}

					//Distancia a val2
					if(labels[track_id] == "val_2"){
						float d2val2 = cv::norm(val2_3d - p);
						if(d2val2 != 0){
							myfile << "," << d2val2;
						}else{
							myfile << ",NULL";
						}
					}else{
						myfile << ",NULL";
					}

				}

				//sino...
				else {
					myfile << ",NULL"; //columna "img_name_"
					myfile << ",NULL,NULL"; //columnas "x_" e "y_"
					myfile << ",NULL"; //columna "r_"
					myfile << ",NULL,NULL";//columnas "vol_real_" y "vol_rep_"
					myfile << ",NULL,NULL"; //columnas "x_rep_" e "y_rep_"
					myfile << ",NULL"; //columna "error_"
					myfile << ",NULL,NULL"; //columnas "x_1cm_" e "y_1cm_"
					myfile << ",NULL"; //columna "d2val1"
					myfile << ",NULL"; //columna "d2val2"

				}
				//fin de fila
				myfile << endl;
			}
		}
	}
	myfile.close();
}



