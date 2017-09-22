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

def plot_graph(links):
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
    node_uls_flow_txt = list(map(lambda x: '%.1f' % x, city_uls_flow))

    left = 0
    up = 0
    scale = 1
    city_point_size = 50
    node_point_size = 50

    plot_ug_flow = False  # 城市地下流量
    plot_cluster = True  # 节点
    plot_link = True  # 边
    plot_city = True  # 城市
    plot_campus = True  # 园区
    plot_circle = False  # 节点区域(虚线的圆)
    title = u''  # 图的题目,可中文,记得别把u删掉

    hdls = []
    if plot_campus:
        camp_legend_hdl = subp.scatter(x=(source_x - left) * scale, y=(source_y - up) * scale, c='r', marker='o',
                                       s=city_point_size, alpha=0.7, label=u'物流园区')
        hdls.append(camp_legend_hdl)

    if plot_city:
        city_legend_hdl = subp.scatter(x=(city_x - left) * scale, y=(city_y - up) * scale, c=city_uls_flow,
                                       vmin=min(city_uls_flow), vmax=max(city_uls_flow), marker='s',
                                       s=city_point_size, alpha=0.7, label=u'地区')
        hdls.append(city_legend_hdl)
        plt.colorbar(city_legend_hdl, fraction=0.05, pad=-0.05, shrink=0.5)

    if plot_ug_flow:
        for i in range(len(node_uls_flow_txt)):
            _x, _y = city_x[i] - 500, city_y[i] + 200
            subp.text(_x, _y, node_uls_flow_txt[i])

    num = 42
    if plot_link:
        for item in links:
            sx = item[0][0]
            sy = item[0][1]
            ex = item[1][0]
            ey = item[1][1]

            tube_legend_hdl = subp.plot([sx, ex], [sy, ey], color='k', lw=2, alpha=0.5)
                                        #label=label)

            # if not hdl_tube_2_added and lineweight == 1:
            #     hdls.append(tube_legend_hdl[0])
            #     hdl_tube_2_added = True
            # elif not hdl_tube_4_added and lineweight == 4:
            #     hdls.append(tube_legend_hdl[0])
            #     hdl_tube_4_added = True
        # import json
        #
        # allcost = 0
        # with open('../data/linksresult/campuslink_{}.json'.format(num), 'r') as cf, \
        #         open('../data/linksresult/links_{}.json'.format(num), 'r') as lf:
        #     campuslink = json.load(cf)
        #     links = json.load(lf)
        #     hdl_tube_2_added = False
        #     hdl_tube_4_added = False
        #
        #     for _, clink in enumerate(campuslink):
        #         if 'campus_axis' not in clink:
        #             allcost += clink['allcost']
        #             continue
        #
        #         cx = clink['campus_axis'][0]
        #         cy = clink['campus_axis'][1]
        #         ex = clink['endnode_axis'][0]
        #         ey = clink['endnode_axis'][1]
        #
        #         if clink['campus_capacity'] > 7200:
        #             lineweight = 4
        #             label = u'双向四轨'
        #         else:
        #             lineweight = 1
        #             label = u'双向双轨'
        #
        #         tube_legend_hdl = subp.plot([cx, ex], [cy, ey], color='k', lw=lineweight, alpha=0.5,
        #                                     label=label)
        #
        #         if not hdl_tube_2_added and lineweight == 1:
        #             hdls.append(tube_legend_hdl[0])
        #             hdl_tube_2_added = True
        #         elif not hdl_tube_4_added and lineweight == 4:
        #             hdls.append(tube_legend_hdl[0])
        #             hdl_tube_4_added = True
        #
        #     for link in links:
        #         if 'node_axis' not in link:
        #             if 'allcost' in link:
        #                 allcost += link['allcost']
        #
        #             continue
        #
        #         lx = link['node_axis'][0]
        #         ly = link['node_axis'][1]
        #
        #         for endnode in link['links']:
        #             elx = endnode['endnode_axis'][0]
        #             ely = endnode['endnode_axis'][1]
        #
        #             if endnode['edgeod'] > 7200:
        #                 lineweight = 4
        #                 label = u'双向四轨'
        #             else:
        #                 lineweight = 1
        #                 label = u'双向双轨'
        #
        #             tube_legend_hdl = subp.plot([lx, elx], [ly, ely], color='k', lw=lineweight, alpha=0.5,
        #                                         label=label)
        #
        #             if not hdl_tube_2_added and lineweight == 1:
        #                 hdls.append(tube_legend_hdl[0])
        #                 hdl_tube_2_added = True
        #             elif not hdl_tube_4_added and lineweight == 4:
        #                 hdls.append(tube_legend_hdl[0])
        #                 hdl_tube_4_added = True

    if plot_cluster:
        with open('../data/kmeansresult/k_clusters_result_919{}.txt'.format(num), 'r') as f:
            pset = set()
            clusters = {}

            for line in f.readlines():
                center = line.split('\t')[0]  # num:x,y
                cid, p = center.split(':')  # x,y

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
                cir = Circle(xy=clu['point'], radius=max(min(clu['maxdist'], 3000), 500), fill=False, ls=linestyle,
                             color=color, alpha=0.7, label=clabel)
                circle_legend_hdl = subp.add_patch(cir)

                if not hdl_circle_1_added and color == 'r':
                    hdls.append(circle_legend_hdl)
                    hdl_circle_1_added = True
                elif not hdl_circle_2_added and color == 'b':
                    hdls.append(circle_legend_hdl)
                    hdl_circle_2_added = True

            node_legend_hdl = subp.scatter(clu['point'][0], clu['point'][1], alpha=0.3, marker='*', s=node_point_size,
                                           color=color, label=nlabel)
            # subp.text(clu['point'][0], clu['point'][1], cid)

            if not hdl_node_1_added and color == 'r':
                hdls.append(node_legend_hdl)
                hdl_node_1_added = True
            elif not hdl_node_2_added and color == 'b':
                hdls.append(node_legend_hdl)
                hdl_node_2_added = True

    # plt.title(u'你好Number: {}, Allcost: {}'.format(num, allcost), fontsize = 16, fontproperties=msyhfont)
    plt.title(title, fontsize=200, fontproperties=msyhfont)

    # formatter = Formatter()
    # formatter.fix_minus('7')
    # subp.xaxis.set_major_formatter(formatter)
    plt.xticks([i for i in range(130000, 170001, 5000)], [i for i in range(130, 171, 5)])
    plt.yticks([i for i in range(145000, 165001, 5000)], [i for i in range(145, 166, 5)])

    # subp.legend(handles=hdls)

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    plt.show()

def store_obj(obj,file_path):
    with open(file_path,'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(file_path):
    if not os.path.exists(file_path):
        return -1
    with open(file_path,'rb') as f:
        return pickle.load(f)

def get_link_dict():
    link_list = load_obj('../data/display_data/tree_links')
    result_dict = {}
    for item in link_list:
        result_dict[len(result_dict)] = item
    return result_dict

def get_top_flow():
    ug_flow_od = np.loadtxt('../data/ug_od.txt')
    top_flow = np.zeros([32,32])
    a_dict = {}
    with open('../data/kmeansresult/k_clusters_result_91942.txt') as read_file:
        for line in read_file:
            items = line.split('\t')
            if len(items)==1:
                continue
            a = int(items[0].split(':')[0])
            b = int(items[1].split(':')[0])
            if a not in a_dict:
                a_dict[a] = set()
            a_dict[a].add(b)
    for i in range(1, 32):
        for j in range(1, 32):
            for m in a_dict[i]:
                for n in a_dict[j]:
                    top_flow[i][j] += ug_flow_od[m][n]##
    return top_flow

def get_flow(connected_subgraph_dict, top_flow):
    sum = 0
    for key in connected_subgraph_dict:
        item = connected_subgraph_dict[key]
        tmpset = set(item)
        for i in item:
            for j in tmpset:
                sum+=top_flow[i][j]
    return sum

def distance(x, y):
    return math.sqrt((x[0]-x[1])**2+(y[0]-y[1])**2)

ug_flow_od = np.loadtxt('../data/ug_od.txt')
link_dict = get_link_dict()
result_list = []
connected_subgraph_dict = {}
top_flow = get_top_flow()

all_length = 0
for key in link_dict:
    all_length += distance(link_dict[key][0][1:], link_dict[key][1][1:])
length_count = 0
while len(link_dict)>0:
    max_length = -1
    tar_key = -1
    tar_dis = -1
    tar_dict = {}
    for key in link_dict:
        item = link_dict[key]
        dis = distance(item[0][1:], item[1][1:])
        a = get_flow(connected_subgraph_dict, top_flow)
        tmp_dict = dict(connected_subgraph_dict)
        i = item[0][0]
        j = item[1][0]
        flag1 = False
        flag2 = False
        key1 = -1
        key2 = -1
        for tkey in tmp_dict:
            item = tmp_dict[tkey]
            if i in item:
                flag1 = True
                key1 = tkey
            if j in item:
                flag2 = True
                key2 = tkey
        if flag1 and flag2:
            tmp_dict[key1].union(tmp_dict[key2])
            tmp_dict.pop(key2)
        else:
            if flag1:
                tmp_dict[key1].add(j)
            if flag2:
                tmp_dict[key2].add(i)
        b = get_flow(tmp_dict, top_flow)
        s = (b-a)*(1-(length_count+dis)/all_length)
        if s>max_length:
            tar_key = key
            tar_dis = dis
            tar_dict = tmp_dict
    tar_item = link_dict[tar_key]
    result_list.append(tar_item)
    length_count += tar_dis
    connected_subgraph_dict = tar_dict
    link_dict.pop(tar_key)

result_list = map(lambda x: map(lambda y: y[1:],x), result_list)
print result_list

plot_list = []
count = 0
cur_length_count = 0
for item in result_list:
    cur_length_count += distance(item[0], item[1])
    if int(cur_length_count*8/all_length)>=len(plot_list):
        plot_list.append([])
        if len(plot_list)!=1:
            plot_list[-1] = list(plot_list[-2])
            diff = cur_length_count - all_length/8*(len(plot_list)-1)
            fac = 1-diff/distance(item[0], item[1])
            x1=item[0][0]
            x2=item[1][0]
            y1=item[0][1]
            y2=item[1][1]
            plot_list[-2].append([item[0], [x1+(x2-x1)*fac, y1+(y2-y1)*fac]])
        plot_list[-1].append(item)
    else:
        plot_list[-1].append(item)
print len(plot_list)
for i in range(8):
    plot_graph(plot_list[i])


