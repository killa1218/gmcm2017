#!/usr/bin/python
# coding=utf8
from __future__ import print_function

from netcampus import build_campus_tube
from netmain import build_area_tube

import sys
sys.path.append('..')

from common.display import visualize


if __name__ == '__main__':
    print('# Build tubes:')
    build_area_tube()
    build_campus_tube()
    print('# Plot and save results:')
    visualize(
        plot_area = False,
        plot_node = True,
        plot_tube = True,
        title = u'运输节点之间的连接结构',
        save_path = '../../res/Question2/tree.png'
    )
    visualize(
        plot_node = True,
        plot_tube = True,
        plot_serve_range = True,
        title = u'最终节点与通道分布图',
        save_path = '../../res/Question2/full.png'
    )

