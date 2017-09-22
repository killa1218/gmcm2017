#!/usr/bin/python
#coding: utf-8

import os
import math
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Circle
from matplotlib.colorbar import Colorbar as cb
from matplotlib.collections import PatchCollection

#!/usr/bin/python3
#coding: utf-8

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Circle
from matplotlib.colorbar import Colorbar as cb
from matplotlib.ticker import Formatter

columns = ['zone no.', 'zone area(km^2)', 'zone area(m^2)', 'center x(m)', 'center y(m)', 'congestion']

# f = open('center_area.csv')
# columns = f.readline().strip().split(',')

ids = np.loadtxt('../data/idx2node.txt')

# row: a send b
ug_flow_od = np.loadtxt('../data/ug_od.txt')
receive_mat = ug_flow_od.transpose()

city_send = ug_flow_od.sum(axis=1)
city_receive = receive_mat.sum(axis=1)

d = np.loadtxt('../data/center_area.csv', skiprows=1, delimiter=',')

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

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

def store_obj(obj,file_path):
    with open(file_path,'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(file_path):
    if not os.path.exists(file_path):
        return -1
    with open(file_path,'rb') as f:
        return pickle.load(f)

source_nodes = NodeGroup([Node(*x) for x in d[:4]])
city_nodes = NodeGroup([Node(*x) for x in d[4:]])

x_min, x_max = d[:, 3].min(), d[:, 3].max()
y_min, y_max = d[:, 4].min(), d[:, 4].max()
# print x_min, x_max, y_min, y_max
x_min, x_max = int(x_min - 2000), int(x_max + 2000)
y_min, y_max = int(y_min - 2000), int(y_max + 2000)
# print x_min, x_max, y_min, y_max

# plt.ion()

fig, subp = plt.subplots()

# bgimg = plt.imread('../map.jpg')
# subp.imshow(bgimg)

plt.rcParams["figure.figsize"] = [(x_max - x_min) / 2000, (y_max - y_min) / 2000]
plt.rcParams['font.sans-serif'] = ['SimHei']
msyhfont = fm.FontProperties(fname='font/msyh.ttf')

source_x, source_y = source_nodes.get_pos()
city_x, city_y = city_nodes.get_pos()
city_congestion = city_nodes.get_congestion()


city_uls_flow = city_send + city_receive
city_uls_flow = city_uls_flow[4:]
node_uls_flow_txt = list(map(lambda x: '%.1f'%x, city_uls_flow))


left = 0
up = 0
scale = 1
city_point_size = 50
node_point_size = 50

plot_ug_flow = False # 城市地下流量
plot_cluster = True # 节点
plot_link = True # 边
plot_city = True # 城市
plot_campus = True # 园区
plot_circle = False # 节点区域(虚线的圆)
title = u'' # 图的题目,可中文,记得别把u删掉

hdls = []
if plot_campus:
    camp_legend_hdl = subp.scatter(x=(source_x - left) * scale, y=(source_y - up) * scale, c='r', marker='o',
                                   s = city_point_size, alpha = 0.7, label = u'物流园区')
    hdls.append(camp_legend_hdl)

if plot_city:
    city_legend_hdl = subp.scatter(x=(city_x - left) * scale, y=(city_y - up) * scale, c=city_uls_flow,
                                   vmin=min(city_uls_flow), vmax=max(city_uls_flow), marker='s',
                                   s = city_point_size, alpha = 0.7, label = u'地区')
    hdls.append(city_legend_hdl)
    plt.colorbar(city_legend_hdl, fraction=0.05, pad=-0.05, shrink=0.5)


if plot_ug_flow:
    for i in range(len(node_uls_flow_txt)):
        _x, _y = city_x[i]-500, city_y[i]+200
        subp.text(_x, _y, node_uls_flow_txt[i])


num = 42
if plot_link:
    import json

    allcost = 0
    with open('../data/linksresult/campuslink_{}.json'.format(num), 'r') as cf, \
            open('../data/linksresult/links_{}.json'.format(num), 'r') as lf:
        campuslink = json.load(cf)
        links = json.load(lf)
        hdl_tube_2_added = False
        hdl_tube_4_added = False

        for _, clink in enumerate(campuslink):
            if 'campus_axis' not in clink:
                allcost += clink['allcost']
                continue

            cx = clink['campus_axis'][0]
            cy = clink['campus_axis'][1]
            ex = clink['endnode_axis'][0]
            ey = clink['endnode_axis'][1]

            if clink['campus_capacity'] > 7200:
                lineweight = 4
                label = u'双向四轨'
            else:
                lineweight = 1
                label = u'双向双轨'

            tube_legend_hdl = subp.plot([cx, ex], [cy, ey], color = 'k', lw = lineweight, alpha = 0.5,
                                        label = label)

            if not hdl_tube_2_added and lineweight == 1:
                hdls.append(tube_legend_hdl[0])
                hdl_tube_2_added = True
            elif not hdl_tube_4_added and lineweight == 4:
                hdls.append(tube_legend_hdl[0])
                hdl_tube_4_added = True

        id_center_links = []
        for link in links:
            if 'node_axis' not in link:
                if 'allcost' in link:
                    allcost += link['allcost']

                continue

            lx = link['node_axis'][0]
            ly = link['node_axis'][1]

            for endnode in link['links']:
                elx = endnode['endnode_axis'][0]
                ely = endnode['endnode_axis'][1]

                id_center_links.append([[link['node_id'], lx, ly], [endnode['endnode'], elx, ely]])

                if endnode['edgeod'] > 7200:
                    lineweight = 4
                    label = u'双向四轨'
                else:
                    lineweight = 1
                    label = u'双向双轨'

                tube_legend_hdl = subp.plot([lx, elx], [ly, ely], color = 'k', lw = lineweight, alpha = 0.5,
                                            label = label)

                if not hdl_tube_2_added and lineweight == 1:
                    hdls.append(tube_legend_hdl[0])
                    hdl_tube_2_added = True
                elif not hdl_tube_4_added and lineweight == 4:
                    hdls.append(tube_legend_hdl[0])
                    hdl_tube_4_added = True

            store_obj(id_center_links, '../data/display_data/tree_links')


if plot_cluster:
    with open('../data/kmeansresult/k_clusters_result_919{}.txt'.format(num), 'r') as f:
        pset = set()
        clusters = {}

        for line in f.readlines():
            center = line.split('\t')[0] # num:x,y
            cid, p = center.split(':') # x,y

            cluster = clusters.setdefault(cid, {})

            if ',' in p:
                contain = line.split('\t')[1]
                cityidx, cp = contain.split(':')
                x, y = p.split(',')
                point = (float(x), float(y))
                pset.add(point)

                cluster['point'] = point
                containlist = cluster.setdefault('contain', [])

                x, y = cp.split(',')
                cpoint = (float(x), float(y))
                containlist.append({'idx': cityidx, 'point': cpoint})

                curmax = cluster.setdefault('maxdist', 0)

                cluster['maxdist'] = max(curmax, distance(point, cpoint))
            else:
                cluster['quantity'] = float(p)

    patches = []
    hdl_circle_1_added = False
    hdl_circle_2_added = False
    hdl_node_1_added = False
    hdl_node_2_added = False
    for cid, clu in clusters.items():
        if clu['quantity'] > 3000:
            color = 'r'
            clabel = u'一级节点服务区域'
            nlabel = u'一级节点'
            linestyle = 'dashed'
        else:
            color = 'b'
            clabel = u'二级节点服务区域'
            nlabel = u'二级节点'
            linestyle = 'dashdot'

        if plot_circle:
            cir = Circle(xy = clu['point'], radius = max(min(clu['maxdist'], 3000), 500), fill = False, ls = linestyle,
                         color = color, alpha = 0.7, label = clabel)
            circle_legend_hdl = subp.add_patch(cir)

            if not hdl_circle_1_added and color == 'r':
                hdls.append(circle_legend_hdl)
                hdl_circle_1_added = True
            elif not hdl_circle_2_added and color == 'b':
                hdls.append(circle_legend_hdl)
                hdl_circle_2_added = True

        node_legend_hdl = subp.scatter(clu['point'][0], clu['point'][1], alpha=0.3, marker='*', s=node_point_size, color = color, label = nlabel)
        # subp.text(clu['point'][0], clu['point'][1], cid)

        if not hdl_node_1_added and color == 'r':
            hdls.append(node_legend_hdl)
            hdl_node_1_added = True
        elif not hdl_node_2_added and color == 'b':
            hdls.append(node_legend_hdl)
            hdl_node_2_added = True

# plt.title(u'你好Number: {}, Allcost: {}'.format(num, allcost), fontsize = 16, fontproperties=msyhfont)
plt.title(title, fontsize = 200, fontproperties=msyhfont)

# formatter = Formatter()
# formatter.fix_minus('7')
# subp.xaxis.set_major_formatter(formatter)
plt.xticks([i for i in range(130000, 170001, 5000)], [i for i in range(130, 171, 5)])
plt.yticks([i for i in range(145000, 165001, 5000)], [i for i in range(145, 166, 5)])

subp.legend(handles = hdls)

plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

plt.show()

# for i in range(5):
#     randd = np.random.random((100, 100))
#     if i == 0:
#         mat = plt.matshow(center_status, vmin=0, vmax=1)
#     else:
#         mat.set_data(center_status)
#     plt.pause(3)
#     plt.draw()


# class Node:
#     def __init__(self, no, akm=0, am=0, x=0, y=0, c=0):
#         self.no = no
#         self.akm = akm
#         self.am = am
#         self.x = x
#         self.y = y
#         self.c = c
#
# class NodeGroup:
#     def __init__(self, arr):
#         self.arr = arr
#
#     def get_pos(self):
#         x_arr = []
#         y_arr = []
#         for c in self.arr:
#             x_arr.append(c.x)
#             y_arr.append(c.y)
#         return np.array(x_arr), np.array(y_arr)
#
#     def get_congestion(self):
#         c_arr = []
#         for c in self.arr:
#             c_arr.append(c.c)
#         return np.array(c_arr)
#
# def distance(point1, point2):
#     return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
#
# def show_uf_by_point():
#     uf = np.loadtxt('../data/display_data/underground_flow')
#     id2node = np.loadtxt('../data/display_data/id2node.txt')
#     center = np.loadtxt('../data/center_area.csv', skiprows=1, delimiter=',')
#
#     uft = uf.transpose()
#     city_send = uf.sum(axis=1)
#     city_receive = uft.sum(axis=1)
#
#     source_nodes = NodeGroup([Node(*x) for x in center[:4]])
#     city_nodes = NodeGroup([Node(*x) for x in center[4:]])
#
#     x_min, x_max = center[:, 3].min(), center[:, 3].max()
#     y_min, y_max = center[:, 4].min(), center[:, 4].max()
#     x_min, x_max = int(x_min - 1000), int(x_max + 1000)
#     y_min, y_max = int(y_min - 1000), int(y_max + 1000)
#
#     fig, subp = plt.subplots()
#
#     plt.rcParams["figure.figsize"] = [(x_max - x_min) / 2000, (y_max - y_min) / 2000]
#     plt.rcParams['font.sans-serif'] = ['SimHei']
#
#     source_x, source_y = source_nodes.get_pos()
#     city_x, city_y = city_nodes.get_pos()
#     city_congestion = city_nodes.get_congestion()
#
#     city_uls_flow = city_send + city_receive
#     city_uls_flow = city_uls_flow[4:]
#     node_uls_flow_txt = list(map(lambda x: '%.1f' % x, city_uls_flow))
#
#     left = 0
#     up = 0
#     scale = 1
#     city_point_size = 10
#     node_point_size = 50
#
#     subp.scatter(x=(source_x - left) * scale, y=(source_y - up) * scale, c='r', marker='o', s=node_point_size, alpha=0.7)
#     subp.scatter(x=(city_x - left) * scale, y=(city_y - up) * scale, c='g', marker='s', s=city_point_size, alpha=0.7)#c=city_uls_flow, vmin=min(city_uls_flow), vmax=max(city_uls_flow)
#
#     for i in range(len(node_uls_flow_txt)):
#         _x, _y = city_x[i]-400, city_y[i]+100
#         subp.text(_x, _y, node_uls_flow_txt[i], fontsize=6)
#
#     plt.xlim(x_min, x_max)
#     plt.ylim(y_min, y_max)
#
#     myfont = fm.FontProperties(fname='/usr/share/fonts/msyh.ttf')
#     plt.title(u'地区中心点分布及需转入地下的最小流量', fontsize = 16, fontproperties=myfont)
#     plt.show()
#
# show_uf_by_point()
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
