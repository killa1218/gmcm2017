#!/usr/bin/python3
#coding: utf-8

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Circle


# row: a send b
ug_flow_od = np.loadtxt('../../res/Question1/uls_od.txt')
receive_mat = ug_flow_od.transpose()

area_send = ug_flow_od.sum(axis=1)
area_receive = receive_mat.sum(axis=1)

d = np.loadtxt('../../data/center_area.csv', skiprows=1, delimiter=',')

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



def visualize(plot_uls_flow = False, plot_node = False, plot_node_id = False, plot_tube = False, plot_area = True,
              plot_campus = True, plot_serve_range = False, title = u'', save_path = None, show = False, num = 42):
    '''
    :param plot_uls_flow: 画出城市地下流量
    :param plot_node: 画出运输节点
    :param plot_node_id: 画出运输节点的ID
    :param plot_tube: 画出运输通道
    :param plot_area: 画出地区
    :param plot_campus: 画出物流园区
    :param plot_serve_range: 画出运输节点服务范围
    :param title: 画图的题目
    :return: 
    '''

    rtn_value = {}

    source_nodes = NodeGroup([Node(*x) for x in d[:4]])
    city_nodes = NodeGroup([Node(*x) for x in d[4:]])

    x_min, x_max = d[:, 3].min(), d[:, 3].max()
    y_min, y_max = d[:, 4].min(), d[:, 4].max()
    x_min, x_max = int(x_min - 2000), int(x_max + 2000)
    y_min, y_max = int(y_min - 2000), int(y_max + 2000)

    plt.rcParams["figure.figsize"] = [(x_max - x_min) / 4000, (y_max - y_min) / 4000]
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['xtick.labelsize'] = 'xx-large'
    plt.rcParams['ytick.labelsize'] = 'xx-large'
    plt.rcParams['axes.labelsize'] = 'x-large'
    msyhfont = fm.FontProperties(fname='../../doc/font/msyh.ttf')

    # plt.ion()

    fig, subp = plt.subplots()

    # bgimg = plt.imread('../map.jpg')
    # subp.imshow(bgimg)

    source_x, source_y = source_nodes.get_pos()
    city_x, city_y = city_nodes.get_pos()
    # city_congestion = city_nodes.get_congestion()

    city_uls_flow = area_send + area_receive
    city_uls_flow = city_uls_flow[4:]
    node_uls_flow_txt = list(map(lambda x: '%.1f'%x, city_uls_flow))


    left = 0
    up = 0
    scale = 1
    city_point_size = 50
    node_point_size = 50

    hdls = []
    if plot_campus:
        camp_legend_hdl = subp.scatter(x=(source_x - left) * scale, y=(source_y - up) * scale, c='r', marker='o',
                                       s = city_point_size, alpha = 0.7, label = u'物流园区')
        hdls.append(camp_legend_hdl)

    if plot_area:
        city_legend_hdl = subp.scatter(x=(city_x - left) * scale, y=(city_y - up) * scale, c=city_uls_flow,
                                       vmin=min(city_uls_flow), vmax=max(city_uls_flow), marker='s',
                                       s = city_point_size, alpha = 0.7, label = u'地区')
        hdls.append(city_legend_hdl)
        plt.colorbar(city_legend_hdl, fraction=0.05, pad=-0.05, shrink=0.5)


    if plot_uls_flow:
        for i in range(len(node_uls_flow_txt)):
            _x, _y = city_x[i]-500, city_y[i]+200
            subp.text(_x, _y, node_uls_flow_txt[i])


    if plot_tube:
        import json

        allcost = 0
        with open('../../res/Question2/campuslink_{}.json'.format(num), 'r') as cf, \
                open('../../res/Question2/links_{}.json'.format(num), 'r') as lf:
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


    if plot_node:
        with open('../../res/Question1/cluster/k_clusters_result_{}.txt'.format(num), 'r') as f:
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

        rtn_value['clusters'] = clusters

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

            if plot_serve_range:
                cir = Circle(xy = clu['point'], radius = max(min(clu['maxdist'], 3000), 500), fill = False,
                             ls = linestyle,color = color, alpha = 0.7, label = clabel)
                circle_legend_hdl = subp.add_patch(cir)

                if not hdl_circle_1_added and color == 'r':
                    hdls.append(circle_legend_hdl)
                    hdl_circle_1_added = True
                elif not hdl_circle_2_added and color == 'b':
                    hdls.append(circle_legend_hdl)
                    hdl_circle_2_added = True

            node_legend_hdl = subp.scatter(clu['point'][0], clu['point'][1], alpha=0.3, marker='*', s=node_point_size,
                                           color = color, label = nlabel)

            if plot_node_id:
                subp.text(clu['point'][0], clu['point'][1], cid)

            if not hdl_node_1_added and color == 'r':
                hdls.append(node_legend_hdl)
                hdl_node_1_added = True
            elif not hdl_node_2_added and color == 'b':
                hdls.append(node_legend_hdl)
                hdl_node_2_added = True

    plt.title(title, fontsize = 16, fontproperties=msyhfont)

    plt.xticks([i for i in range(130000, 170001, 5000)], [i for i in range(130, 171, 5)])
    plt.yticks([i for i in range(145000, 165001, 5000)], [i for i in range(145, 166, 5)])

    subp.legend(handles = hdls)

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    subp.set_xlabel('×1000', fontsize = 7)
    subp.set_ylabel('×1000', fontsize = 7)
    subp.xaxis.set_label_coords(1.0, -0.012)
    subp.yaxis.set_label_coords(-0.01, 1)

    if save_path:
        plt.savefig(save_path)
        print('Figure saved in {}'.format(save_path))

    if show or not save_path:
        plt.show()

    return rtn_value
