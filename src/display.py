import numpy as np
import matplotlib.pyplot as plt

columns = ['zone no.', 'zone area(km^2)', 'zone area(m^2)', 'center x(m)', 'center y(m)', 'congestion']

# f = open('center_area.csv')
# columns = f.readline().strip().split(',')

ids = [1,2,3,4,791,792,793,794,795,796,797,798,799,800,801,802,803,804,805,806,807,808,809,810,811,812,813,814,815,816,817,818,819,820,821,822,823,824,825,826,827,828,829,830,831,832,833,834,835,836,837,838,839,840,841,842,843,844,845,846,847,848,849,850,851,852,853,854,855,856,857,858,859,860,861,862,863,864,865,866,867,868,869,870,871,872,873,874,875,876,877,878,879,880,881,882,883,884,885,886,887,888,889,890,891,892,893,894,895,896,897,898,899,900]

# row: a send b
send_mat = np.loadtxt('OD_data.csv', skiprows=1, delimiter=',')[:, 1:]
receive_mat = send_mat.transpose()

node_send = send_mat.sum(axis=1)
node_receive = receive_mat.sum(axis=1)

d = np.loadtxt('center_area.csv', skiprows=1, delimiter=',')

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
plt.rcParams["figure.figsize"] = [(x_max - x_min)/2000,(y_max - y_min)/2000]

source_x, source_y = source_nodes.get_pos()
city_x, city_y = city_nodes.get_pos()
city_congestion = city_nodes.get_congestion()

node_uls_flow = (node_send + node_receive)[4:] * (city_congestion - 4) / city_congestion
node_uls_flow[node_uls_flow < 0] = 0
node_uls_flow_txt = map(lambda x: '%.1f'%x, node_uls_flow)

class kmeans:
    def __init__(self, k, radius, eps=1e-6):
        self.k = k
        self.radius = radius
        # self.nodes = nodes
        randx = np.random.random(k) * (x_max - x_min) + x_min
        randy = np.random.random(k) * (y_max - y_min) + y_min
        self.centers = NodeGroup([Node(no=i+1, x=randx[i], y=randy[i]) for i in range(k)])

    def fit(self, nodes):
        pass

plt.scatter(x=source_x, y=source_y, c='r', marker='s')
plt.scatter(x=city_x, y=city_y, c=city_congestion, vmin=0, vmax=10, marker='s')
for i in range(len(node_uls_flow_txt)):
    _x, _y = city_x[i]-500, city_y[i]+200
    plt.text(_x, _y, node_uls_flow_txt[i])
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.colorbar(fraction=0.05, pad=-0.05, shrink=0.6)
plt.show()

# for i in range(5):
#     randd = np.random.random((100, 100))
#     if i == 0:
#         mat = plt.matshow(center_status, vmin=0, vmax=1)
#     else:
#         mat.set_data(center_status)
#     plt.pause(3)
#     plt.draw()
