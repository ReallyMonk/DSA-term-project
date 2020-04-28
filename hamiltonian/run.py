#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-04-10 20:04:38
@LastEditTime: 2020-04-19 22:29:25
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# the code is inspired by some github snake projects
# and I re-implement them in my idea.

import argparse
import numpy as np

from hamiltonian.game import Game, GameConf

if __name__ == '__main__':
    res = []
    for i in range(8, 17, 2):
        runtimes = []
        counts = []
        for k in range(5):

            conf = GameConf(map_rows=i)
            conf.solver_name = "HamiltonSolver"
            # print("Algorithm: %s  " % (conf.solver_name))

            G = Game(conf)
            G.run()
            runtimes.append(G.total_time)
            counts.append(G.count)
            # print('total_time: ', G.total_time)
            # print('total move: ', G.count)

        res.append((np.mean(counts), i**2-3, np.mean(runtimes)))
    print(res)
