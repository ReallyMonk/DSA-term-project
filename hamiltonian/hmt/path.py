from collections import deque

import random
from hamiltonian.map_snake import Direc, PointType
from hamiltonian.hmt.base import BaseSolver
import sys

class C:

    def __init__(self):
        self.reset()

    def reset(self):
        # Shortest path
        self.parent = None
        self.dist = sys.maxsize
        # Longest path
        self.visit = False


class PathSolver(BaseSolver):

    def __init__(self, snake):
        super().__init__(snake)
        self._information = [[C() for _ in range(snake.map.num_cols)]
                       for _ in range(snake.map.num_rows)]

    @property
    def information(self):
        return self._information

    def shortest_food(self):
        return self.path_to(self.map.food, "shortest")

    def long_tail(self):
        return self.path_to(self.snake.tail(), "longest")

    def path_to(self, end, path_type):
        ori_type = self.map.point(end).type
        self.map.point(end).type = PointType.EMPTY
        if path_type == "shortest":
            path = self.shortest_path_to(end)
        elif path_type == "longest":
            path = self.longest_to(end)
        self.map.point(end).type = ori_type
        return path

    def shortest_path_to(self, end):
        self._reset_table()

        head = self.snake.head()
        self._information[head.x][head.y].dist = 0
        queue = deque()
        queue.append(head)

        while queue:
            now = queue.popleft()
            if now == end:
                return self._build_path(head, end)

            # now == head
            if now == head:
                first_direc = self.snake.direc
            else:
                first_direc = self._information[now.x][now.y].parent.direc_to(now)
            ajds = now.all_adj()
            # print(ajds)
            
            # random adjecent node
            random.shuffle(ajds)
            for i, pos in enumerate(ajds):
                if first_direc == now.direc_to(pos):
                    ajds[0], ajds[i] = ajds[i], ajds[0]
                    break

            # Traverse adjacent positions
            for pos in ajds:
                if self._is_valid(pos):
                    adj_cell = self._information[pos.x][pos.y]
                    if adj_cell.dist == sys.maxsize:
                        adj_cell.parent = now
                        adj_cell.dist = self._information[now.x][now.y].dist + 1
                        queue.append(pos)

        return deque()

    def longest_to(self, end):
        path = self.shortest_path_to(end)
        if not path:
            return deque()

        self._reset_table()
        now = head = self.snake.head()

        self._information[now.x][now.y].visit = True
        for direc in path:
            now = now.adj(direc)
            self._information[now.x][now.y].visit = True

        idx, now = 0, head
        while 1:
            cur_direc = path[idx]
            nxt = now.adj(cur_direc)  

            if cur_direc == Direc.LEFT or cur_direc == Direc.RIGHT:
                tests = [Direc.UP, Direc.DOWN]
            elif cur_direc == Direc.UP or cur_direc == Direc.DOWN:
                tests = [Direc.LEFT, Direc.RIGHT]

            extended = False
            for test_direc in tests:
                cur_test = now.adj(test_direc)
                nxt_test = nxt.adj(test_direc)
                if self._is_valid(cur_test) and self._is_valid(nxt_test):
                    self._information[cur_test.x][cur_test.y].visit = True
                    self._information[nxt_test.x][nxt_test.y].visit = True
                    path.insert(idx, test_direc)
                    path.insert(idx + 2, Direc.opposite(test_direc))
                    extended = True
                    break

            if not extended:
                now = nxt
                idx += 1
                if idx >= len(path):
                    break

        return path

    def _reset_table(self):
        for row in self._information:
            for col in row:
                col.reset()

    def _build_path(self, src, end):
        path = deque()
        tmp = end
        while tmp != src:
            parent = self._information[tmp.x][tmp.y].parent
            path.appendleft(parent.direc_to(tmp))
            tmp = parent
        return path

    def _is_valid(self, pos):
        return self.map.is_safe(pos) and not self._information[pos.x][pos.y].visit
