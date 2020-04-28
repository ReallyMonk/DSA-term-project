
import numpy
import time

from hamiltonian.hmt.path import PathSolver

from hamiltonian.map_snake import Direc
from hamiltonian.hmt.base import BaseSolver

class Infom:

    def __init__(self):
        self.idx = None
        self.direc = Direc.NONE


class HamiltonSolver(BaseSolver):

    def __init__(self, snake, shortcuts=True):
        
        super().__init__(snake)

        self._shortcuts = shortcuts
        self._solverpath = PathSolver(snake)
        self._information = [[Infom() for _ in range(snake.map.num_cols)]
                        for _ in range(snake.map.num_rows)]
        import time
        start = time.time()
        self._build_ham()
        print('build hamilton cycle need: ', time.time() - start, 's')

    @property
    def information(self):
        return self._information
    def dis(self, a, x, b):
        if a > x:
            x += b
        return x - a
    def next_direc(self):
        # Take shorcuts when the snake is not too long
        if self._shortcuts and self.snake.len() < 0.5 * self.map.capacity:
            head = self.snake.head()  # head.x head.y is position
            x = self.information[head.x][head.y].direc  # information is row x clos, .idx .direc
            if self._solverpath.shortest_food():
                tail, nxt, food = self.snake.tail(), head.adj(self._solverpath.shortest_food()[0]), self.map.food
                tail_idx = self.information[tail.x][tail.y].idx
                head_idx = self.information[head.x][head.y].idx
                nxt_idx = self.information[nxt.x][nxt.y].idx
                food_idx = self.information[food.x][food.y].idx
                # Exclude one exception
                if not (len(self._solverpath.shortest_food()) == 1 and abs(food_idx - tail_idx) == 1):
                    head_idx_rel = self.dis(tail_idx, head_idx, self.map.capacity)
                    nxt_idx_rel = self.dis(tail_idx, nxt_idx, self.map.capacity)
                    food_idx_rel = self.dis(tail_idx, food_idx, self.map.capacity)
                    if nxt_idx_rel > head_idx_rel and nxt_idx_rel <= food_idx_rel:
                        x = self._solverpath.shortest_food()[0]
        #print('nxt_direc:', nxt_direc)
        return x
    # not short cut : 100: 0.0024
    # short cut : 100: 0.74
    def _build_ham(self):
        """Build a hamiltonian cycle on the map."""
        path = self._solverpath.long_tail()
        print(path)
        current, k = self.snake.head(), 0
        for direc in path:
            self.information[current.x][current.y].idx = k
            self.information[current.x][current.y].direc = direc
            current = current.adj(direc)
            k += 1
        # Process snake bodies
        current = self.snake.tail()
        for _ in range(self.snake.len() - 1):
            self.information[current.x][current.y].idx = k
            self.information[current.x][current.y].direc = self.snake.direc
            current = current.adj(self.snake.direc)
            k += 1

    
