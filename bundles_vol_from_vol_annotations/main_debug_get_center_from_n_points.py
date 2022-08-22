from itertools import combinations
from statistics import mean
import cv2
from xml.dom import minidom
import numpy as np
import pandas as pd
import math


def get_centre_radius_circle_from_3points(pts):
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


def parse_str_points_to_float_list(str_points):
    str_points = str_points.replace(';', ',')
    pts = [float(p) for p in str_points.split(",")]
    return pts

def get_centre_radius_circle_from_n_points(pts):
    n_points = len(pts) // 2
    combs = combinations(range(n_points), 3)
    h = []
    k = []
    r = []
    for comb in combs:
        pts_aux = [pts[comb[0] * 2], pts[comb[0] * 2 + 1], pts[comb[1] * 2], pts[comb[1] * 2 + 1], pts[comb[2] * 2],
                   pts[comb[2] * 2 + 1]]
        h_aux, k_aux, r_aux = get_centre_radius_circle_from_3points(pts_aux)
        h.append(h_aux)
        k.append(k_aux)
        r.append(r_aux)
    return mean(h), mean(k), mean(r)

def get_centres_and_radius_circle_from_n_points(pts):
    n_points = len(pts) // 2
    combs = combinations(range(n_points), 3)
    h = []
    k = []
    r = []
    for comb in combs:
        pts_aux = [pts[comb[0] * 2], pts[comb[0] * 2 + 1], pts[comb[1] * 2], pts[comb[1] * 2 + 1], pts[comb[2] * 2],
                   pts[comb[2] * 2 + 1]]
        h_aux, k_aux, r_aux = get_centre_radius_circle_from_3points(pts_aux)
        h.append(h_aux)
        k.append(k_aux)
        r.append(r_aux)
    return h, k, r

def draw_circles(img, labels,i):
    # img = img.permute(1, 2, 0).numpy()
    # img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    for label in labels:
        x, y, r = label
        color = (23,220, 75)
        thickness = 1
        lineType = cv2.LINE_8
        shift = 0
        img = cv2.circle(img.copy(), (int(x.item()),int(y.item())), int(r), color, thickness)
        cv2.imwrite(str(i)+".png",img)

def draw_sub_circles(img, labels, labels2, i):
    # img = img.permute(1, 2, 0).numpy()
    # img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

    for label in labels:
        x, y, r = label
        color = (23,220, 75)
        thickness = 1
        img = cv2.circle(img.copy(), (int(x.item()),int(y.item())), int(r), color, thickness)
        cv2.imwrite(str(i)+"c.png", img)
    if i > 3:
        for label2 in labels2:
            label2 = np.squeeze(label2)
            for l in label2:
                x, y, r = np.squeeze(l)
                color = (255, 255, 0)
                thickness = 1
                img = cv2.circle(img.copy(), (int(x.item()), int(y.item())), int(r), color, thickness)
                cv2.imwrite(str(i) + "c.png", img)


if __name__ == "__main__":
    annotations =["/mnt/datos/onedrive/Doctorado/3df/scripts/circle_from_n_points_debug/3puntos/annotations.xml",
                  "/mnt/datos/onedrive/Doctorado/3df/scripts/circle_from_n_points_debug/4puntos/annotations.xml",
                  "/mnt/datos/onedrive/Doctorado/3df/scripts/circle_from_n_points_debug/5puntos/annotations.xml",
                  "/mnt/datos/onedrive/Doctorado/3df/scripts/circle_from_n_points_debug/6puntos/annotations.xml"
                ]
    img_path = "/mnt/datos/onedrive/Doctorado/3df/scripts/VID_20220217_101111_F0.png"
    an = 3
    img = cv2.imread(img_path)
    for annotation in annotations:
        xmldoc = minidom.parse(annotation)
        image = xmldoc.getElementsByTagName('image')[0]
        width_img = int(image.attributes["width"].value)
        height_img = int(image.attributes["height"].value)
        points_list = image.getElementsByTagName('points')
        print(f"iteración {an}")

        labels = np.zeros((11, 3))
        labels2 = np.zeros((11, 3, int(math.factorial(an)/(math.factorial(3)*(math.factorial(an-3))))))

        for i, points in enumerate(points_list):
            str_points = points.attributes['points'].value
            pts = parse_str_points_to_float_list(str_points)
            labels[i, :] = get_centre_radius_circle_from_n_points(pts)
            labels2[i, :, :] = get_centres_and_radius_circle_from_n_points(pts)
        # draw_circles(img, labels, an)
        draw_sub_circles(img, labels, labels2, an)
        an += 1
