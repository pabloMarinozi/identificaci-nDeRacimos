import pandas as pd
import os
from abc import ABC, abstractmethod
class OutputManager(ABC):
    def __init__(self, output_path):
        self.output_path = output_path

    def generate_df_tracks_csv(self,df_tracks):
        pass


    def generate_bundles_for_image(self,df_tracks):
        if df_tracks is not None:
            df_tracks_group = df_tracks.groupby('img_name_0', as_index=False)
            for name, df_group in df_tracks_group:
                name = name.replace("_F0.png", "")
                name = name.replace("_F-1.png", "")
                name = name.replace("_F3.png", "")
                name = name.replace("_F4.png", "")

                df_group['track_id'] = range(0,len(df_group))
                df_group["nro_kf"] = 2
                path = os.path.join(self.output_path, name, "bundles.csv")
                print(path)
                try:
                    df_group.to_csv(path, index=False)
                except OSError:
                    print(f"WARNING: el directorio {path[:-11]} no existe")

class OutputManagerFecovita(OutputManager):
    def __init__(self, output_path):
        self.output_path = output_path

    def generate_df_tracks_csv(self,df_tracks):

        # df_temp = df_tracks.loc[df_tracks.index.duplicated(keep='first')]
        # if len(df_temp)>0:
        #     print("  WARNING: indices duplicados en df_tracks. Solo se mantiene la primera de las filas duplicadas")
        #     print(df_temp)
        #     df_tracks = df_tracks.loc[~df_tracks.index.duplicated(keep='first')]

        df_tracks_left = df_tracks[df_tracks['side']==0].copy()
        df_tracks_left = df_tracks_left.set_index('group_id')
        df_tracks_right = df_tracks[df_tracks['side']==1].copy()
        df_tracks_right = df_tracks_right.set_index('group_id')
        df_tracks = pd.merge(df_tracks_left, df_tracks_right, on='group_id')
        df_tracks.reset_index(inplace=True)

        columns_df = ["track_id","img_name_0","label_0","x_0","y_0","r_0","side_0","img_name_1","label_1","x_1","y_1","r_1","side_1"]
        df_tracks.columns = columns_df

        df_tracks["nro_kf"] = 2

        columns_df = ["track_id","label_0","nro_kf","img_name_0","x_0","y_0","r_0","img_name_1","x_1","y_1","r_1"]
        df_tracks = df_tracks[columns_df]

        columns_df = ["track_id","label","nro_kf","img_name_0","x_0","y_0","r_0","img_name_1","x_1","y_1","r_1"]
        df_tracks.columns = columns_df

        path = os.path.join(self.output_path, "bundle_cvat.csv")
        print("GUARDANDO tracks en "+ path)
        df_tracks.to_csv(path)

        return df_tracks

class OutputManagerFecovitaCompleteflag(OutputManager):
    def __init__(self, output_path):
        self.output_path = output_path

    def generate_df_tracks_csv(self, df_tracks):

        # df_temp = df_tracks.loc[df_tracks.index.duplicated(keep='first')]
        # if len(df_temp)>0:
        #     print("  WARNING: indices duplicados en df_tracks. Solo se mantiene la primera de las filas duplicadas")
        #     print(df_temp)
        #     df_tracks = df_tracks.loc[~df_tracks.index.duplicated(keep='first')]

        df_tracks_left = df_tracks[df_tracks['side']==0].copy()
        df_F0 = df_tracks_left.copy()
        df_tracks_left = df_tracks_left.set_index('group_id')
        df_tracks_right = df_tracks[df_tracks['side']==1].copy()
        df_tracks_right = df_tracks_right.set_index('group_id')
        df_tracks = pd.merge(df_tracks_left, df_tracks_right, on='group_id')
        df_tracks.reset_index(inplace=True)
        df_tracks.drop(['complete_x', 'complete_y'], axis=1, inplace=True)

        columns_df = ["track_id","img_name_0","label_0","x_0","y_0","r_0","side_0","img_name_1","label_1","x_1","y_1","r_1","side_1"]
        df_tracks.columns = columns_df

        df_tracks["nro_kf"] = 2

        columns_df = ["track_id","label_0","nro_kf","img_name_0","x_0","y_0","r_0","img_name_1","x_1","y_1","r_1"]
        df_tracks = df_tracks[columns_df]

        columns_df = ["track_id","label","nro_kf","img_name_0","x_0","y_0","r_0","img_name_1","x_1","y_1","r_1"]
        df_tracks.columns = columns_df

        path = os.path.join(self.output_path, "bundle_cvat.csv")
        print("GUARDANDO tracks en "+ path)
        df_tracks.to_csv(path)

        df_F0.drop(['side', 'group_id'], axis=1, inplace=True)
        df_F0.to_csv(os.path.join(self.output_path, 'labels_for_coco.csv'))
        return df_tracks

class Output_Strategy:
    @staticmethod
    def get_output_manager(output_path, point_strategy):

            if point_strategy == "fecovita":
                return OutputManagerFecovita(output_path)
            if point_strategy == "fecovita_just_right":
                return OutputManagerFecovita(output_path)
            if point_strategy == "fecovita_with_complete_flag":
                return OutputManagerFecovitaCompleteflag(output_path)
