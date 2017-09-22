#!/usr/bin/python
# coding=utf8
from __future__ import print_function
from __future__ import absolute_import

from calculate_uls_flow import calculate
from cluster import cluster

import sys
sys.path.append('..')

from common.display import visualize


if __name__ == '__main__':
    print('# Calculate ULS flow:')
    calculate()
    print('# Cluster areas and set nodes:')
    cluster()
    print('# Plot and save results:')
    visualize(
        plot_uls_flow = True,
        title = u'地区中心点分布及需转入地下的最小流量',
        save_path = '../../res/Question1/total_uls_flow.png'
    )
    res = visualize(
        plot_node = True,
        plot_serve_range = True,
        title = u'一级节点和二级节点的分布',
        save_path = '../../res/Question1/nodes.png'
    )

    result_dict = {}
    for cid, clu in res['clusters'].items():
        type = 0
        if clu['quantity'] > 3000:
            type = 1
        else:
            type = 2
        result_dict[int(cid)] = [int(cid), type, clu['point'][0], clu['point'][1], max(min(clu['maxdist'], 3000), 500),
                             clu['quantity']]
    for i in range(1, 32):
        print(result_dict[i])

    import xlwt
    from tempfile import TemporaryFile

    book = xlwt.Workbook()
    sheet1 = book.add_sheet('节点分布')
    for i in range(1, 32):
        for j in range(1, 7):
            sheet1.write(i, j, float(result_dict[i][j - 1]))
    name = "../../res/Question1/node_result.xls"
    book.save(name)
    book.save(TemporaryFile())
