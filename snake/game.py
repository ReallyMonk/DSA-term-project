#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0111,W0201,W0703

import errno
import os
import traceback
from enum import Enum, unique

from snake.base import Direc, Map, PointType, Pos, Snake
from snake.gui import GameWindow
from snake.solver import GreedySolver, HamiltonSolver
import time

class GameConf:

    def __init__(self, map_rows = 16, algorithm_name = 'HamiltonSolver'):
        """Initialize a default configuration."""

        # Solver
        self._algorithm_name = algorithm_name  # Class name of the solver

        # Size
        self.map_rows = map_rows
        self.map_cols = self.map_rows
        self.map_width = 320  # pixels
        self.map_height = self.map_width
        self.window_width = self.map_width
        self.window_height = self.map_height
        self.grid_pad_ratio = 0.1

        # Switch
        self.show_grid_line = True
        self.show_info_panel = True

        # Delay
        self.interval_draw = 1  # ms
        self.interval_draw_max = 1  # ms

        # Color
        self.color_bg = '#000000'
        self.color_line = '#424242'
        self.color_wall = '#F5F5F5'
        self.color_food = '#DC143C'
        self.color_head = '#F5F5F5'
        self.color_body = '#F5F5F5'

        # Initial snake
        self.init_direc = Direc.RIGHT
        self.init_bodies = [Pos(1, 4), Pos(1, 3), Pos(1, 2), Pos(1, 1)]
        self.init_types = [PointType.HEAD_R] + [PointType.BODY_HOR] * 3

    @property
    def algorithm_name(self):
        return self._algorithm_name

class Game:
    def __init__(self, conf):
        self._conf = conf
        self._map = Map(conf.map_rows + 2, conf.map_cols + 2)
        self._snake = Snake(self._map, conf.init_direc,
                            conf.init_bodies, conf.init_types)
        print(globals())
        self._algorithm = globals()[self._conf.algorithm_name](self._snake)
        print(self._algorithm)
        self.count = 0
        self.total_time = 0.0
        self.creat_food = 1

    @property
    def snake(self):
        return self._snake

    def run(self):

        # window = GameWindow("Self-playing Snake Game", self._conf, self._map, self)
        # window.show(self._game_main_normal)
        while not self._is_episode_end():
            self._game_main_normal()

    def _game_main_normal(self):
        if not self._map.has_food():
            self._map.create_rand_food()
            self.creatfood += 1

        if self._is_episode_end():
            return

        start = time.time()
        next = self._algorithm.next_direc()
        end = time.time()
        self.count += 1
        self.total_time += (end - start)
        print('total_time', self.total_time)
        print('move times: ', self.count)

        self._update_direc(next)

        self._snake.move()

    def _update_direc(self, new_direc):
        self._snake.direc_next = new_direc

    def _is_episode_end(self):
        return self._snake.dead or self._map.is_full()

