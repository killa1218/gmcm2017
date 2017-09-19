import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection

columns = ['zone no.', 'zone area(km^2)', 'zone area(m^2)', 'center x(m)', 'center y(m)', 'congestion']

# f = open('center_area.csv')
# columns = f.readline().strip().split(',')

ids = np.loadtxt('../data/idx2node.txt')

# row: a send b
send_mat = np.loadtxt('../data/od.txt')
receive_mat = send_mat.transpose()

node_send = send_mat.sum(axis=1)
node_receive = receive_mat.sum(axis=1)

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

plt.rcParams["figure.figsize"] = [(x_max - x_min)/2000,(y_max - y_min)/2000]
# plt.rcParams["figure.figsize"] = [(x_max - x_min),(y_max - y_min)]

source_x, source_y = source_nodes.get_pos()
city_x, city_y = city_nodes.get_pos()
city_congestion = city_nodes.get_congestion()


node_uls_flow = (node_send + node_receive)[4:] * (city_congestion - 4) / city_congestion
node_uls_flow[node_uls_flow < 0] = 0
node_uls_flow_txt = list(map(lambda x: '%.1f'%x, node_uls_flow))


left = 0
up = 0
scale = 1


subp.scatter(x=(source_x - left) * scale, y=(source_y - up) * scale, c='r', marker='s')
subp.scatter(x=(city_x - left) * scale, y=(city_y - up) * scale, c=city_congestion, vmin=0, vmax=10, marker='s')

# for i in range(len(node_uls_flow_txt)):
#     _x, _y = city_x[i]-500, city_y[i]+200
    # subp.text(_x, _y, node_uls_flow_txt[i])

with open('../data/kmeansresult/k_clusters_result35.txt', 'r') as f:
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
for cid, clu in clusters.items():
    if clu['quantity'] > 3000:
        color = 'r'
    else:
        color = 'b'

    cir = Circle(xy = clu['point'], radius = min(clu['maxdist'], 3000), fill = False, ls = 'dashed', color = color)
    # cir = Circle(xy = clu['point'], radius = 3000, fill = False, ls = 'dashed')

    subp.add_patch(cir)

plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
# subp.colorbar(fraction=0.05, pad=-0.05, shrink=0.6)
plt.show()

# for i in range(5):
#     randd = np.random.random((100, 100))
#     if i == 0:
#         mat = plt.matshow(center_status, vmin=0, vmax=1)
#     else:
#         mat.set_data(center_status)
#     plt.pause(3)
#     plt.draw()
