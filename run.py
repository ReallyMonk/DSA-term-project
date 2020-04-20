#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-04-10 20:04:38
@LastEditTime: 2020-04-10 21:27:32
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from snake.game import Game, GameConf

dict_solver = {
    "greedy": "GreedySolver",
    "hamilton": "HamiltonSolver"
}

parser = argparse.ArgumentParser(description="Run snake game agent.")
parser.add_argument("-s", default="hamilton", choices=dict_solver.keys(),
                    help="name of the solver to direct the snake (default: hamilton)")
args = parser.parse_args()

if __name__ == '__main__':
    conf = GameConf(map_rows = 8)
    conf.solver_name = dict_solver[args.s]
    print("Algorithm: %s  " % (conf.solver_name))

    G = Game(conf)
    G.run()
    print('total_time: ', G.total_time)
    print('total move: ', G.count)
