from abc import ABC, abstractmethod
import math
from itertools import combinations
from statistics import mean


def get_centre_radius_circle_from_n_points(pts):
    n_points = len(pts) // 2
    combs = combinations(range(n_points), 3)
    h = []
    k = []
    r = []
    for comb in combs:
        pts_aux = [pts[comb[0] * 2], pts[comb[0] * 2 + 1], pts[comb[1] * 2], pts[comb[1] * 2 + 1], pts[comb[2] * 2],
                   pts[comb[2] * 2 + 1]]
        h_aux, k_aux, r_aux = self.get_centre_radius_circle_from_3points(self, pts_aux)
        h.append(h_aux)
        k.append(k_aux)
        r.append(r_aux)
    return mean(h), mean(k), mean(r)

if __name__ == "__main__":
    pass