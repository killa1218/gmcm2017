#!/usr/bin/python
#coding: utf-8

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Circle
from matplotlib.colorbar import Colorbar as cb
from matplotlib.collections import PatchCollection

class Node:
    def __init__(self, no, akm=0, am=0, x=0, y=0, c=0):
        self.no = no
        self.akm = akm
        self.am = am
        self.x = x
        self.y = y
        self.c = c

class NodeGroup:
    def __init__(self, arr):
        self.arr = arr

    def get_pos(self):
        x_arr = []
        y_arr = []
        for c in self.arr:
            x_arr.append(c.x)
            y_arr.append(c.y)
        return np.array(x_arr), np.array(y_arr)

    def get_congestion(self):
        c_arr = []
        for c in self.arr:
            c_arr.append(c.c)
        return np.array(c_arr)

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def show_uf_by_point():
    uf = np.loadtxt('../data/display_data/underground_flow')
    id2node = np.loadtxt('../data/display_data/id2node.txt')
    center = np.loadtxt('../data/center_area.csv', skiprows=1, delimiter=',')

    uft = uf.transpose()
    city_send = uf.sum(axis=1)
    city_receive = uft.sum(axis=1)

    source_nodes = NodeGroup([Node(*x) for x in center[:4]])
    city_nodes = NodeGroup([Node(*x) for x in center[4:]])

    x_min, x_max = center[:, 3].min(), center[:, 3].max()
    y_min, y_max = center[:, 4].min(), center[:, 4].max()
    x_min, x_max = int(x_min - 1000), int(x_max + 1000)
    y_min, y_max = int(y_min - 1000), int(y_max + 1000)

    fig, subp = plt.subplots()

    plt.rcParams["figure.figsize"] = [(x_max - x_min) / 2000, (y_max - y_min) / 2000]
    plt.rcParams['font.sans-serif'] = ['SimHei']

    source_x, source_y = source_nodes.get_pos()
    city_x, city_y = city_nodes.get_pos()
    city_congestion = city_nodes.get_congestion()

    city_uls_flow = city_send + city_receive
    city_uls_flow = city_uls_flow[4:]
    node_uls_flow_txt = list(map(lambda x: '%.1f' % x, city_uls_flow))

    left = 0
    up = 0
    scale = 1
    city_point_size = 10
    node_point_size = 50

    subp.scatter(x=(source_x - left) * scale, y=(source_y - up) * scale, c='r', marker='o', s=node_point_size, alpha=0.7)
    subp.scatter(x=(city_x - left) * scale, y=(city_y - up) * scale, c='g', marker='s', s=city_point_size, alpha=0.7)#c=city_uls_flow, vmin=min(city_uls_flow), vmax=max(city_uls_flow)

    for i in range(len(node_uls_flow_txt)):
        _x, _y = city_x[i]-400, city_y[i]+100
        subp.text(_x, _y, node_uls_flow_txt[i], fontsize=6)

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    myfont = fm.FontProperties(fname='/usr/share/fonts/msyh.ttf')
    plt.title(u'地区中心点分布及需转入地下的最小流量', fontsize = 16, fontproperties=myfont)
    plt.show()

show_uf_by_point()
#
# with open('../data/kmeansresult/k_clusters_result_91950.txt', 'r') as f:
#     pset = set()
#     clusters = {}
#
#     for line in f.readlines():
#         center = line.split('\t')[0]  # num:x,y
#         cid, p = center.split(':')  # x,y
#
#         cluster = clusters.setdefault(cid, {})
#
#         if ',' in p:
#             contain = line.split('\t')[1]
#             cityidx, cp = contain.split(':')
#             x, y = p.split(',')
#             point = (float(x), float(y))
#             pset.add(point)
#
#             cluster['point'] = point
#             containlist = cluster.setdefault('contain', [])
#
#             x, y = cp.split(',')
#             cpoint = (float(x), float(y))
#             containlist.append({'idx': cityidx, 'point': cpoint})
#
#             curmax = cluster.setdefault('maxdist', 0)
#
#             cluster['maxdist'] = max(curmax, distance(point, cpoint))
#         else:
#             cluster['quantity'] = float(p)
#
# patches = []
# for cid, clu in clusters.items():
#     if clu['quantity'] > 3000:
#         color = 'r'
#     else:
#         color = 'b'
#
#     cir = Circle(xy=clu['point'], radius=max(min(clu['maxdist'], 3000), 500), fill=False, ls='dashed', color=color)
#     # cir = Circle(xy = clu['point'], radius = 3000, fill = False, ls = 'dashed')
#
#     subp.add_patch(cir)
#     subp.scatter(clu['point'][0], clu['point'][1], alpha=0.3, marker='*', s=node_point_size, color=color)
#
# # subp.legend()

# plt.xlim(x_min, x_max)
# plt.ylim(y_min, y_max)
#
# myfont = fm.FontProperties(fname='/usr/share/fonts/msyh.ttf')
# plt.title(u'地区中心点分布及需转入地下的最小流量', fontproperties=myfont)
# plt.show()

# for i in range(5):
#     randd = np.random.random((100, 100))
#     if i == 0:
#         mat = plt.matshow(center_status, vmin=0, vmax=1)
#     else:
#         mat.set_data(center_status)
#     plt.pause(3)
#     plt.draw()
