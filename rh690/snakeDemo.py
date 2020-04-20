#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-04-09 15:01:42
@LastEditTime: 2020-04-19 21:00:34
'''
from random import sample
import math
import numpy as np
import os
import time
import dfsSolver as bfs
# block_num = 8


class Snake():
    def __init__(self, block_num, initBody=None):
        self.dir = -1
        self.bn2 = block_num + 2
        self.body = [0] * self.bn2**2
        # initBody = [31, 41, 42, 43]
        self.len = 0
        if not initBody:
            halfN = len(self.body) // 2
            initBody = [halfN + i for i in range(-4, -1)]
        for i in range(len(initBody) - 1, 0, -1):
            self.body[initBody[i]] = initBody[i - 1]
            self.len += 1
        for i in range(self.bn2**2):
            x, y = i % self.bn2, i // self.bn2
            if x == 0 or x == (self.bn2 - 1) or y == 0 or y == (self.bn2 - 1):
                self.body[i] = 1
        self.head = self.body[initBody[0]] = initBody[0]
        self.tail = initBody[-1]
        self.oldtail = initBody[-1] + 1
        self.path = []
        # print(self)

        # create a slover
        self.solver = bfs.bfsSolver()
        self.generateFood()
        self.TEMP = (initBody, self.food, self.path)

    def pass_info(self):
        self.solver.update_info(self.head, self.tail, self.body.copy(),
                                self.food, self.bn2)
        return

    def move(self):
        #self.pass_info()
        if not self.changDir():
            return False
        oldhead = self.head
        self.head += self.dir
        if self.body[self.head]:
            print('lost!')
            return False
            # pass
        self.body[self.head] = self.body[oldhead] = self.head
        if self.head != self.food:
            self.oldtail = self.tail
            self.body[self.tail], self.tail = 0, self.body[self.tail]
            return self.head, self.oldtail
        else:
            #print('score++')
            self.len += 1
            self.generateFood()
            #print('food', self.food)
            return self.head, None, self.food
        return True

    def up(self):
        self.dir = -self.bn2
        self.move()

    def down(self):
        self.dir = self.bn2
        self.move()

    def left(self):
        self.dir = -1
        self.move()

    def right(self):
        self.dir = +1
        self.move()

    def changDir(self):
        self.pass_info()
        self.path = self.solver.find_path()

        if len(self.path):
            self.dir = self.path.pop() - self.head
        else:
            # print('out of path')
            return False
        return True

    def __str__(self):
        num = int(math.sqrt(len(self.body)))
        res = ''
        for i in range(num):
            temp = self.body[i * num:(i + 1) * num]
            res += str(temp)[1:-1] + "\n"
        return res

    def generateFood(self):
        grid_size = len(self.body)
        empty = [i for i in range(grid_size) if not self.body[i]]
        if not empty:
            print('win')
            return
        self.food = sample(empty, 1)[0]
        #print('food at:{}'.format(self.food))

        #self.move()
        #print('path', self.path)
        #print(self)
        #input()


if __name__ == '__main__':
    all_time = []
    score = []

    for i in range(8, 17):
        tmp_time = []
        tmp_score = []
        print('current map size is ', i)
        for k in range(50):
            # create snake game
            print(i, k)
            snake = Snake(i)
            # play
            t0 = time.time()
            while snake.move():
                pass

            t1 = time.time()

            tmp_time.append(t1 - t0)
            tmp_score.append(snake.len)

        all_time.append(np.mean(tmp_time))
        score.append(np.mean(tmp_score))

    print(all_time)
    print(score)

'''
if __name__ == "__main__":
    snake = Snake(10)

    while snake.move():
        pass'''
