#!/usr/bin/python
# coding=utf8
from __future__ import print_function

from ..common.display import visualize


if __name__ == '__main__':
    print('# Plot and save results:')
    visualize(
        plot_node_id = True,
        plot_node = True,
        plot_serve_range = True,
        plot_tube = True,
        title=u'节点与通道',
        save_path='../../res/Question3/nodes_and_tubes.png',
        show = True
    )
