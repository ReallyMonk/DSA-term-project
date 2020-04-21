#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-04-10 20:04:38
@LastEditTime: 2020-04-19 22:24:12
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103

from snake.base import Direc
from snake.solver.base import BaseSolver
from snake.solver.path import PathSolver
import time


class _TableCell:

    def __init__(self):
        self.idx = None
        self.direc = Direc.NONE


class HamiltonSolver(BaseSolver):

    def __init__(self, snake, shortcuts=True):
        if snake.map.num_rows % 2 != 0 or snake.map.num_cols % 2 != 0:
            raise ValueError("num_rows and num_cols must be even.")
        super().__init__(snake)

        self._shortcuts = shortcuts
        self._path_solver = PathSolver(snake)
        self._table = [[_TableCell() for _ in range(snake.map.num_cols)]
                        for _ in range(snake.map.num_rows)]
        import time
        start = time.time()
        self._build_cycle()
        print('build hamilton cycle need: ', time.time() - start, 's')

    @property
    def table(self):
        return self._table

    def next_direc(self):
        head = self.snake.head() # head.x head.y is position
        nxt_direc = self._table[head.x][head.y].direc # _table is row x clos, .idx .direc

        # Take shorcuts when the snake is not too long
        if self._shortcuts and self.snake.len() < 0.5 * self.map.capacity:
            path = self._path_solver.shortest_path_to_food()  # directions in path
            if path:
                tail, nxt, food = self.snake.tail(), head.adj(path[0]), self.map.food
                tail_idx = self._table[tail.x][tail.y].idx
                head_idx = self._table[head.x][head.y].idx
                nxt_idx = self._table[nxt.x][nxt.y].idx
                food_idx = self._table[food.x][food.y].idx
                # Exclude one exception
                if not (len(path) == 1 and abs(food_idx - tail_idx) == 1):
                    head_idx_rel = self._relative_dist(tail_idx, head_idx, self.map.capacity)
                    nxt_idx_rel = self._relative_dist(tail_idx, nxt_idx, self.map.capacity)
                    food_idx_rel = self._relative_dist(tail_idx, food_idx, self.map.capacity)
                    if nxt_idx_rel > head_idx_rel and nxt_idx_rel <= food_idx_rel:
                        nxt_direc = path[0]
        #print('nxt_direc:', nxt_direc)
        return nxt_direc
    # not short cut : 100: 0.0024
    # short cut : 100: 0.74
    def _build_cycle(self):
        """Build a hamiltonian cycle on the map."""
        path = self._path_solver.longest_path_to_tail()
        print(path)
        cur, cnt = self.snake.head(), 0
        for direc in path:
            self._table[cur.x][cur.y].idx = cnt
            self._table[cur.x][cur.y].direc = direc
            cur = cur.adj(direc)
            cnt += 1
        # Process snake bodies
        cur = self.snake.tail()
        for _ in range(self.snake.len() - 1):
            self._table[cur.x][cur.y].idx = cnt
            self._table[cur.x][cur.y].direc = self.snake.direc
            cur = cur.adj(self.snake.direc)
            cnt += 1

    def _relative_dist(self, ori, x, size):
        if ori > x:
            x += size
        return x - ori
