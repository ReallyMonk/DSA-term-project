#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-04-10 20:14:28
@LastEditTime: 2020-04-19 13:55:16
'''
from tkinter import *
# from import Thread, Lock
from snakeDemo import *
import threading
import time


class CanvasDemo:
    def __init__(self, block_num=20, block_size=20):
        window = Tk()
        window.title("Canvas Demo")
        window.resizable(width=False, height=False)
        self.bn2 = block_num+2
        self.bs = block_size

        canvas_wh = block_size*block_num
        self.canvas = Canvas(window, width=canvas_wh, height=canvas_wh,
                             bg="black", highlightthickness=0)
        self.canvas.pack()
        # self.lock = Lock()

        self.snake = Snake(block_num)
        # self.snake.body[56] = 1
        print(self.snake)
        body, food, path = self.snake.TEMP
        # print(body, food)
        del self.snake.TEMP
        for i in body:
            self.drawRect(i, 'white')
            time.sleep(0.1)
            self.canvas.update()
        for p in path:
            self.drawRect(p, 'green')
            time.sleep(0.1)
            self.canvas.update()
        self.drawRect(food, 'red')
        # self.loop()
        # self.canvas.after(1000, self.loop)
        plot = self.snake.move()
        while plot:
            flag = len(plot)
            if flag == 3:
                self.drawRect(plot[0], 'white')
                # for p in plot[1]:
                #     self.drawRect(p, 'green')
                self.drawRect(plot[2], 'red')
            elif flag == 2:
                self.drawRect(plot[0], 'white')
                self.drawRect(plot[1], 'black')
            
            time.sleep(0.1)
            self.canvas.update()
            plot = self.snake.move()
        
        print('over')

        window.mainloop()
    
    def gameThread(self, plot):
        nextstep = self.snake.move()

    def loop(self):
        path = self.snake.move()
        # if path:
        #     self.path = path
        # else:
            
        # if not plot:
        #     print('over')
        #     return
        # flag = len(plot)
        # if flag == 3:
        #     self.drawRect(plot[0], 'white')
        #     # for p in plot[1]:
        #     #     self.drawRect(p, 'green')
        #     self.drawRect(plot[2], 'red')
        # elif flag == 2:
        #     self.drawRect(plot[0], 'white')
        #     self.drawRect(plot[1], 'black')
        
        time.sleep(0.05)
        self.canvas.update()
        self.loop()

        # self.canvas.after(50, self.loop)

    def drawRect(self, N, color):
        N = N - self.bn2 - 1
        # bn2 = self.bn+2
        x, y = N % self.bn2, N // self.bn2
        self.canvas.create_rectangle(
            x*self.bs, y*self.bs, (x+1)*self.bs, (y+1)*self.bs, fill=color)


CanvasDemo(8)
