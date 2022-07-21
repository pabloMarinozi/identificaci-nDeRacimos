from naming_strategies import Naming_Strategy_Factory
from point_parsing_strategies import Point_Parsing_Strategy_Factory
import pandas as pd

class CVat_xml_Parser:
    def __init__(self, xmldoc, naming_strategy, point_strategy):
        self.imagesList = xmldoc.getElementsByTagName('image')
        self.naming_strategy = Naming_Strategy_Factory.get_naming_strategy(naming_strategy)
        self.point_parsing_strategy = Point_Parsing_Strategy_Factory.get_point_parsing_strategy(point_strategy)


    def get_bundles(self):
        data_bundles_list = []
        for image in self.imagesList:
            id_img = image.attributes["id"].value
            #if int(id_img) < 89 and int(id_img) > 104: continue
            path_img = image.attributes["name"].value
            width_img = int(int(image.attributes["width"].value)/2) #divide el ancho en dos porque son imágenes fusionadas a lo ancho
            height_img = int(image.attributes["height"].value)
            base_name_left, base_name_right = self.naming_strategy.get_basename(path_img)
            
            points_list = image.getElementsByTagName('points')
            list_of_point_dicts = self.point_parsing_strategy.parse_points(id_img,points_list, width_img, height_img, base_name_left, base_name_right)
            df = pd.DataFrame(list_of_point_dicts)
            data_bundles_list.append(df)
        return pd.concat(data_bundles_list)



