#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-04-09 15:01:42
@LastEditTime: 2020-04-13 12:05:13
'''
from random import sample
import math
import numpy as np
import os
import time
from Astar import *
# block_num = 8


class Snake():
    def __init__(self, block_num, initBody=None):
        self.dir = -1
        self.bn2 = block_num + 2
        self.body = [0]*self.bn2**2
        # initBody = [31, 41, 42, 43]
        self.len = 0
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
        print(self)
        self.generateFood()
        self.TEMP = (initBody, self.food, self.path)

    def move(self):
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
            # print('score++')
            self.len += 1
            # input('eat')
            self.generateFood()
            print('food', self.food)
            # flag = True
            return self.head, None, self.food
        # print(self.len)
        # print(self)
        return True
        # if flag:
        #     return self.path

    def up(self):
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
        if len(self.path):
            self.dir = self.path.pop() - self.head
        else:
            if self.len > (self.bn2-2)**2//3:
                self.path = self.astar.find(
                    self.oldtail, self.head, self.tail, self.body, self.oldtail, 1, 1)
            else:
                self.path = self.astar.find(
                    self.food, self.head, self.tail, self.body, self.oldtail)
            if not self.path:
                print(self.food)
                print(self.head, self.tail, self.oldtail)
                print(self)
                return False
            self.dir = self.path.pop()-self.head
        return True

    def __str__(self):
        num = int(math.sqrt(len(self.body)))
        res = ''
        for i in range(num):
            temp = self.body[i * num: (i + 1) * num]
            res += str(temp)[1:-1]+"\n"
        return res

    def generateFood(self):
        grid_size = len(self.body)
        empty = [i for i in range(grid_size) if not self.body[i]]
        if not empty:
            print('win')
            return
        self.food = sample(empty, 1)[0]
        print('food at:{}'.format(self.food))
        if self.len > (self.bn2-2)**2//3:
            self.path = self.astar.find(
                self.oldtail, self.head, self.tail, self.body, self.oldtail, 1, 1)
        else:
            self.path = self.astar.find(
                self.food, self.head, self.tail, self.body, self.oldtail)


if __name__ == '__main__':
    snake = Snake(10)
    # print(snake)
    # path = pf.find(snake.food, snake.head, snake.tail, snake.body)
    # print(path)
    while snake.move():
        # print(snake)
        # print(snake.head, snake.tail, snake.oldtail)
        # input()
        pass
        # print('food at:{}'.format(snake.food))
        # snake.move()
        # time.sleep(0.05)
        # key = input()

        # if key == '':
        #     snake.move()
        #     print(snake)
        # elif key == 'r':
        #     snake.right()
        # elif key == 'u':
        #     snake.up()
        # elif key == 'd':
        #     snake.down()
        # else:
        #     continue
