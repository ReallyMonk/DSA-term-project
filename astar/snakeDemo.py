#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-04-09 15:01:42
@LastEditTime: 2020-04-19 15:33:29
'''
from random import sample
import math
import numpy as np
import os
import time
from Astar import *
from time import perf_counter
# block_num = 8


class Snake():
    def __init__(self, block_num, initBody=None):
        self.dir = -1
        self.bn2 = block_num + 2
        self.body = [0]*self.bn2**2
        # initBody = [31, 41, 42, 43]
        self.len = 1
        if not initBody:
            halfN = len(self.body) // 2
            initBody = [halfN+i for i in range(-4, -1)]
        for i in range(len(initBody) - 1, 0, -1):
            self.body[initBody[i]] = initBody[i - 1]
            self.len += 1
        for i in range(self.bn2**2):
            x, y = i % self.bn2, i // self.bn2
            if x == 0 or x == (self.bn2 - 1) or y == 0 or y == (self.bn2 - 1):
                self.body[i] = 1
        self.head = self.body[initBody[0]] = initBody[0]
        self.tail = initBody[-1]
        self.oldtail = initBody[-1]+1
        self.astar = Astar(block_num)
        self.path = []
        self.pathIndex = 0
        self.generateFood()
        self.TEMP = (initBody, self.food, self.path)

    def move(self):
        if not self.changDir():
            return False
        oldhead = self.head
        self.head += self.dir
        if self.body[self.head]:
            return False
        self.body[self.head] = self.body[oldhead] = self.head
        if self.head != self.food:
            self.oldtail = self.tail
            self.body[self.tail], self.tail = 0, self.body[self.tail]
            return self.head, self.oldtail
        else:
            # print('score++')
            self.len += 1
            # input('eat')
            self.generateFood()
            # flag = True
            return self.head, None, self.food
        # print(self.len)
        # print(self)
        return True
        # if flag:
        #     return self.path

    def up(self):
        # self.changDir('up')
        # self.
        self.move()

    def down(self):
        self.changDir('down')
        self.move()

    def left(self):
        self.changDir('left')
        self.move()

    def right(self):
        self.changDir('right')
        self.move()

    def changDir(self):
        # flag = False
        # if self.pathIndex == -1:
        #     # print('empty')
        #     if self.len > (self.bn2-2)**2//3:
        #         self.path = self.astar.find(
        #             self.oldtail, self.head, self.tail, self.body, self.oldtail, 1, 1)
        #         self.pathIndex = len(self.path)-1
        #     else:
        #         self.path = self.astar.find(
        #             self.food, self.head, self.tail, self.body, self.oldtail)
        #         self.pathIndex = len(self.path)-1
        #     flag = True
        # # else:
        # self.dir = self.path[self.pathIndex] - self.head
        # self.pathIndex -= 1
        # return flag
        if len(self.path):
            self.dir = self.path.pop() - self.head
        else:
            # if self.len > (self.bn2-2)**2//3:
            #     self.path = self.astar.find(
            #         self.oldtail, self.head, self.tail, self.body, self.oldtail, 1, 1)
            # else:
            self.path = self.astar.find(
                    self.food, self.head, self.tail, self.body, self.oldtail)
            if not self.path:
                return False
            self.dir = self.path.pop()-self.head
        return True

    def __str__(self):
        num = int(math.sqrt(len(self.body)))
        res = ''
        for i in range(num):
            temp = self.body[i * num: (i + 1) * num]
            # res += str([i and 1 for i in temp])[1:-1]+"\n"
            res += str(temp)[1:-1]+"\n"
        return res

    def generateFood(self):
        grid_size = len(self.body)
        empty = [i for i in range(grid_size) if not self.body[i]]
        if not empty:
            return
        self.food = sample(empty, 1)[0]
        # self.food = 72
        # self.food = 51
        # self.body[self.food] = 1
        # print('food at:{}'.format(self.food))
        # if self.len > (self.bn2-2)**2//3:
        #     self.path = self.astar.find(
        #         self.oldtail, self.head, self.tail, self.body, self.oldtail, 1, 1)
        # else:
        self.path = self.astar.find(
            self.food, self.head, self.tail, self.body, self.oldtail)

    def score(self):
        return self.len-3


if __name__ == '__main__':
    for i in range(8, 17):
        scores = []
        runtimes = []
        # print(i)
        for k in range(10):

            snake = Snake(i)
            start = perf_counter()
            while snake.move():
                pass
            end = perf_counter()
            scores.append(snake.score())
            runtimes.append(end-start)
        print(i, np.average(scores), np.average(runtimes))

    # snake = Snake(8)
    # print(snake.score())
    # print(snake.oldtail)
    # while snake.move():
    #     print(snake)
    #     pass
    # print(snake.score())
