# _*_ coding: utf-8 _*_
"""
Time:     2023/6/21 16:13
Author:   Liyuan Meng(Sophia)
Version:  V 0.1
File:     generate_grid.py
Describe: 
"""

import numpy as np
from configuration import num_orders, conservative_factor, vol_factor


# generate price grid
def generate_uni_grid(price, vol, trend):
    grid = np.arange(num_orders + 1)
    grids_up = vol_factor * vol * grid[1:]
    grids_down = -grids_up
    if trend == 1:
        grids = price + np.concatenate((grids_down, np.zeros(1), conservative_factor * grids_up))
    elif trend == -1:
        grids = price + np.concatenate((conservative_factor * grids_down, np.zeros(1), grids_up))
    else:
        grids = price + np.concatenate((grids_down, np.zeros(1), grids_up))

    return np.round(grids, decimals=3)


def generate_geo_grid(price, vol, trend):
    grids_up = np.geomspace(1, (num_orders + 1) * vol_factor * vol / price + 1, num_orders + 1)[1:]
    grids_down = 2 - grids_up
    if trend == 1:
        grids = price * np.concatenate((grids_down, np.ones(1), conservative_factor * grids_up - conservative_factor + 1))
    elif trend == -1:
        grids = price * np.concatenate((conservative_factor * grids_down - conservative_factor + 1, np.ones(1), grids_up))
    else:
        grids = price * np.concatenate((grids_down, np.ones(1), grids_up))

    return np.round(grids, decimals=3)


# generate position
def generate_position(price, grids):
    if price < grids[0]:
        return num_orders
    elif price >= grids[2 * num_orders]:
        return -num_orders
    else:
        for i in range(2 * num_orders):
            if grids[i] <= price < grids[i + 1]:
                if i < num_orders:
                    return num_orders - i - 1
                else:
                    return num_orders - i

