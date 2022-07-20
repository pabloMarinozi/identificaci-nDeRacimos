from abc import ABC, abstractmethod
import math

## Strategy interface
class Point_Parsing_Strategy(ABC):
    def get_centre_radius_circle_from_3points(self,pts):
        x1 = pts[0]
        x2 = pts[2]
        x3 = pts[4]
        y1 = pts[1]
        y2 = pts[3]
        y3 = pts[5]

        x12 = x1 - x2
        x13 = x1 - x3

        y12 = y1 - y2
        y13 = y1 - y3

        y31 = y3 - y1
        y21 = y2 - y1

        x31 = x3 - x1
        x21 = x2 - x1

        # x1^2 - x3^2
        sx13 = pow(x1, 2) - pow(x3, 2)

        # y1^2 - y3^2
        sy13 = pow(y1, 2) - pow(y3, 2)

        sx21 = pow(x2, 2) - pow(x1, 2)
        sy21 = pow(y2, 2) - pow(y1, 2)

        f = (((sx13) * (x12) + (sy13) *
                (x12) + (sx21) * (x13) +
                (sy21) * (x13)) // (2 *
                ((y31) * (x12) - (y21) * (x13))))
                    
        g = (((sx13) * (y12) + (sy13) * (y12) +
                (sx21) * (y13) + (sy21) * (y13)) //
                (2 * ((x31) * (y12) - (x21) * (y13))))

        c = (-pow(x1, 2) - pow(y1, 2) -
                2 * g * x1 - 2 * f * y1)

        # eqn of circle be x^2 + y^2 + 2*g*x + 2*f*y + c = 0
        # where centre is (h = -g, k = -f) and
        # radius r as r^2 = h^2 + k^2 - c
        h = -g
        k = -f

        sqr_of_r = h * h + k * k - c
        # r is the radius
        r = round(math.sqrt(sqr_of_r), 5)

        return h, k, r

    def parse_str_points_to_float_list(self,str_points):
        str_points = str_points.replace(';', ',')
        pts = [float(p) for p in str_points.split(",")] 
        return pts

    def getDictPoint(self,name_right, name_left, label, width_img, height_img, x, y, r, group_id):
        # Si x es mayor al ancho de la imagen, entonces el punto corresponde a la imagen
        # de la derecha, sino a la imagen de la izquierda
        side = 0
        base_name = ""
        if (x > width_img):
            x = x-width_img 
            base_name = name_right
            side = 1
        else:
            base_name = name_left

        # Si la imagen está vertical aplica una transformación a los puntos para  
        # pasar el punto del espacio vertical al horizontal
        if (width_img < height_img):
            temp_x = x
            temp_y = y
            x = y
            y = width_img-temp_x
            if (x < 0): 
                print("  WARNING: coordenada negativa:")
                print(base_name, label, temp_x, temp_y, width_img, height_img, x, y)

        dict = {'base_name': base_name, 
                'label':label,  
                'x': int(x), 
                'y': int(y), 
                'r': str(r), 
                'group_id': group_id,
                'side': side}
        
        return dict

    @abstractmethod
    def parse_points(self, id_img, points_list, width_img, height_img, base_name_left, base_name_right):
        pass

## Concrete strategies
class Strategy_Fecovita(Point_Parsing_Strategy):
    def __init__(self):
        self.group_id_vals = 10000

    def parse_points(self, id_img, points_list, width_img, height_img, base_name_left, base_name_right):
        if (len(points_list) == 0):
           print("  WARNING: no se encontraron etiquetas para la imagen", base_name_left)
        list_of_dicts = []
        
        for points in points_list:
            label = points.attributes['label'].value
            group_id = ""
            if (label != "radio_baya" and 
                    label != "val_cm2_1" and label != "val_cm2_2" and 
                    label != "val_in2_1" and label != "val_in2_2"):
                try:
                    group_id = int(points.attributes['group_id'].value)
                except KeyError:
                    print("  WARNING: point sin 'group_id' en", base_name_left, ". Error manual de etiquetado:", label)
                    continue
            if label == "baya":
                group_id = ""
                try:
                    group_id = int(points.attributes['group_id'].value)
                except KeyError:
                    print("  WARNING: point de tipo 'baya' sin 'group_id' en", base_name_left, "(error manual de etiquetado)")
                    continue

                # Extrae los punto de elemento 'points' con label 'baya' y calcula su centro
                str_points = points.attributes['points'].value
                #print(str_points)
                pts = super().parse_str_points_to_float_list(str_points)
                # x, y, r = get_centre_radius_circle_from_3points(pts[0:6])

                x = 0
                y = 0
                r = 0
                dict = {}
                
                # Si se trata de una etiqueta 'points' con 3 puntos
                if len(pts) == 6:
                    x, y, r = super().get_centre_radius_circle_from_3points(pts)
                    dict = super().getDictPoint(base_name_right, base_name_left, label, 
                                        width_img, height_img, x, y, r, group_id)
                    list_of_dicts.append(dict)

                # Si se trata de una etiqueta 'points' con 4 puntos
                elif len(pts) == 8:
                    list_x = [pts[0],pts[2],pts[4],pts[6]]
                    x_right = max(list_x)
                    if x_right < width_img:
                    	print("El punto con id ",attr_id," tiene x ",x_right, " pero el ancho de la imagen es ", width_img)
                    x_right_index = pts.index(x_right)
                    y_right = pts[x_right_index+1]
                    pts.remove(x_right)
                    pts.remove(y_right)
                    x, y, r = super().get_centre_radius_circle_from_3points(pts)
                    dict = super().getDictPoint(base_name_right, base_name_left, label,
                        width_img, height_img, x, y, r, group_id)
                    list_of_dicts.append(dict)

                    x = x_right
                    y = y_right
                    r = "NULL"
                    dict = super().getDictPoint(base_name_right, base_name_left, label, 
                                        width_img, height_img, x, y, r, group_id)
                    list_of_dicts.append(dict)
                
                else:
                    print("  WARNING: etiqueta 'points' de cvat con", len(pts), "puntos")
            elif (label == "keyframe" or label == "keypoint" ):
                    # or label == "val_cm2_1" or label == "val_cm2_2" 
                    # or label == "val_in2_1" or label == "val_in2_2"):
                
                # Correcciones en los nombres de etiquetas
                if label == "keyframe": 
                    label = "keypoint"


                # Extrae los punto de elemento 'points'
                str_points = points.attributes['points'].value
                pts = super().parse_str_points_to_float_list(str_points)
               
                # Si se trata de una etiqueta 'points' con más de 1 punto
                if len(pts) > 2:
                    print("  WARNING: etiqueta 'points' de cvat con", int(len(pts)/2), "puntos. Se descarta" , label)
                    continue

                x = pts[0]
                y = pts[1]
                r = "NULL"
                dict = super().getDictPoint(base_name_right, base_name_left, label, 
                                    width_img, height_img, x, y, r, group_id)
                list_of_dicts.append(dict)
            elif (label == "val_cm2_1" or label == "val_cm2_2" 
                     or label == "val_in2_1" or label == "val_in2_2" 
                    or label == "cm_1" or label == "cm_2"):

                # Correcciones en los nombres de etiquetas
                if label == "val_cm2_1": 
                    label = "val_1"
                if label == "val_cm2_2": 
                    label = "val_2"
                if label == "cm_1": 
                    label = "cal_1"
                if label == "cm_2": 
                    label = "cal_2"

                # Extrae los punto de elemento 'points'
                str_points = points.attributes['points'].value
                pts = super().parse_str_points_to_float_list(str_points)

                # Si se trata de una etiqueta 'points' con más de 2 puntos
                if len(pts) > 4:
                    print("  WARNING: etiqueta 'points' de cvat con", int(len(pts)/2), "puntos. Se descarta" , label)
                    continue

                x = pts[0]
                y = pts[1]
                r = "NULL"
                dict = super().getDictPoint(base_name_right, base_name_left, label, 
                    width_img, height_img, x, y, r, self.group_id_vals)
                list_of_dicts.append(dict)

                x = pts[2]
                y = pts[3]
                r = "NULL"
                dict = super().getDictPoint(base_name_right, base_name_left, label, 
                    width_img, height_img, x, y, r, self.group_id_vals)
                list_of_dicts.append(dict)

                self.group_id_vals = self.group_id_vals+1
        return list_of_dicts


class Strategy_Fecovita_Just_Right(Point_Parsing_Strategy):
    def __init__(self):
        self.group_id_vals = 10000

    def parse_points(self, id_img, points_list, width_img, height_img, base_name_left, base_name_right):
        if (len(points_list) == 0):
           print("  WARNING: no se encontraron etiquetas para la imagen", base_name_left)
        list_of_dicts = []
        
        for points in points_list:
            label = points.attributes['label'].value
            attributes = points.getElementsByTagName('attribute')
            attr_id = ""
            for attr in attributes:
                if attr.getAttribute("name")=='id':
                    attr_id = id_img + "_" + attr.firstChild.nodeValue

            if (label != "radio_baya" and 
                    label != "val_cm2_1" and label != "val_cm2_2" and 
                    label != "val_in2_1" and label != "val_in2_2"):
                try:
                    group_id = int(points.attributes['group_id'].value)
                except KeyError:
                    print("  WARNING: point sin 'group_id' en", base_name_left, ". Error manual de etiquetado:", label)
                    continue
            if label == "baya":
                group_id = ""
                try:
                    group_id = int(points.attributes['group_id'].value)
                except KeyError:
                    print("  WARNING: point de tipo 'baya' sin 'group_id' en", base_name_left, "(error manual de etiquetado)")
                    continue

                # Extrae los punto de elemento 'points' con label 'baya' y calcula su centro
                str_points = points.attributes['points'].value
                #print(str_points)
                pts = super().parse_str_points_to_float_list(str_points)
                # x, y, r = get_centre_radius_circle_from_3points(pts[0:6])

                x = 0
                y = 0
                r = 0
                dict = {}

                # Si se trata de una etiqueta 'points' con 4 puntos
                if len(pts) == 8:
                    list_x = [pts[0],pts[2],pts[4],pts[6]]
                    x_right = max(list_x)
                    if x_right < width_img:
                    	print("El punto con id ",attr_id," tiene x ",x_right, " pero el ancho de la imagen es ", width_img)
                    x_right_index = pts.index(x_right)
                    y_right = pts[x_right_index+1]

                    r = "NULL"
                    dict = super().getDictPoint(base_name_right, base_name_left, label, 
                                        width_img, height_img, x_right, y_right, r, attr_id)
                    list_of_dicts.append(dict)
                
                else:
                    print("  WARNING: etiqueta 'points' de cvat con", len(pts), "puntos")
            elif (label == "val_cm2_1" or label == "val_cm2_2" 
                     or label == "val_in2_1" or label == "val_in2_2" 
                    or label == "cm_1" or label == "cm_2"):

                # Correcciones en los nombres de etiquetas
                if label == "val_cm2_1": 
                    label = "val_1"
                if label == "val_cm2_2": 
                    label = "val_2"
                if label == "cm_1": 
                    label = "cal_1"
                if label == "cm_2": 
                    label = "cal_2"

                # Extrae los punto de elemento 'points'
                str_points = points.attributes['points'].value
                pts = super().parse_str_points_to_float_list(str_points)

                # Si se trata de una etiqueta 'points' con más de 2 puntos
                if len(pts) > 4:
                    print("  WARNING: etiqueta 'points' de cvat con", int(len(pts)/2), "puntos. Se descarta" , label)
                    continue
                list_x = [pts[0],pts[2]]
                x_right = max(list_x)
                if x_right < width_img:
                	print("El punto con id ",attr_id," tiene x ",x_right, " pero el ancho de la imagen es ", width_img)
                x_right_index = pts.index(x_right)
                y_right = pts[x_right_index+1]
                r = "NULL"
                dict = super().getDictPoint(base_name_right, base_name_left, label, 
                    width_img, height_img, x_right, y_right, r, attr_id)
                list_of_dicts.append(dict)

                self.group_id_vals = self.group_id_vals+1
        return list_of_dicts


## Strategy factory
class Point_Parsing_Strategy_Factory:
    @staticmethod
    def get_point_parsing_strategy(strategy_name):
        if strategy_name=="fecovita":
            return Strategy_Fecovita()
        if strategy_name=="fecovita_just_right":
            return Strategy_Fecovita_Just_Right()
