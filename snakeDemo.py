#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-04-09 15:01:42
@LastEditTime: 2020-04-10 14:12:45
'''
from random import sample
import math
import numpy as np
from Astar import *
block_num = 8
D = {
    'up': -(block_num+2),
    'down': block_num+2,
    'left': -1,
    'right': +1
}

class Snake():
    def __init__(self, block_num, init=[36, 37, 38]):
        self.dir = 'left'
        bn2 = block_num+2
        self.body = [0]*bn2**2
        for i in range(len(init) - 1, 0, -1):
            self.body[init[i]] = init[i - 1]
        for i in range(bn2**2):
            x, y = i % bn2, i // bn2
            if x == 0 or x == (bn2 - 1) or y == 0 or y == (bn2 - 1):
                self.body[i] = 1
        self.head = self.body[init[0]] = init[0]
        self.tail = init[-1]
        self.astar = Astar(block_num)
        self.generateFood()
        # self.food = 33

    def move(self):
        oldhead = self.head
        self.head += D[self.dir]
        if self.body[self.head]:
            print('lost!')
            return
            # pass
        self.body[self.head] = self.body[oldhead] = self.head
        if self.head != self.food:
            self.body[self.tail], self.tail = 0, self.body[self.tail]

        else:
            print('score++')
            self.generateFood()
        print(self)

    def up(self):
        self.changDir('up')
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

    def changDir(self, dir):
        self.dir = dir

    def __str__(self):
        num = int(math.sqrt(len(self.body)))
        res = ''
        for i in range(num):
            res += str(self.body[i*num:(i+1)*num])[1:-1]+"\n"
        return res

    def generateFood(self):
        grid_size = len(self.body)
        empty = [i for i in range(grid_size) if not self.body[i]]
        self.food = sample(empty, 1)[0]
        print('food at:{}'.format(self.food))
        print('astar: ', str(self.astar.find(
            self.food, self.head, self.tail, self.body))[1:-1])


if __name__ == '__main__':
    snake = Snake(block_num)
    print(snake)
    # path = pf.find(snake.food, snake.head, snake.tail, snake.body)
    # print(path)
    while True:
        print('food at:{}'.format(snake.food))
        key = input()
        if key == 'l':
            snake.left()
        elif key == 'r':
            snake.right()
        elif key == 'u':
            snake.up()
        elif key == 'd':
            snake.down()
        else:
            continue
