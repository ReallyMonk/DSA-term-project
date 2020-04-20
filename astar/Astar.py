#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-04-09 20:37:07
@LastEditTime: 2020-04-19 21:49:32
'''
from queue import PriorityQueue
import numpy as np
import math


class Astar:
    class ghostSnake:       # at every branch, send a ghost snake to all its neighbor blocks
        def __init__(self, head, cost, prehead, tail, body, LongestPath, pretail=None):
            self.head = head
            self.cost = cost
            self.body = body.copy()
            self.body[prehead] = head
            self.body[head] = head
            if not pretail:
                self.pretail = tail
                self.tail = body[tail]
                self.body[tail] = LongestPath
            else:
                self.pretail = pretail
                self.tail = tail

        def __lt__(self, other):    # less than, used in prioritu queue
            return self.cost < other.cost

    def __init__(self, block_num):  # based on block_num, setup some hyperparameters
        self.dis_weight = 1         # different weight factors has different behavior
        self.step_weight = 1        # step_weigth=0 --> greedy, dis_weight=0 --> bfs
        self.bn2 = block_num+2
        self.dirs = [-self.bn2, self.bn2, -1, +1]   # directions
        self.flag = 1

    def distance(self, A, B):       # computate distance for int A and int B (one dim to two dims)
        disX, disY = A % self.bn2 - \
            B % self.bn2, A//self.bn2-B//self.bn2
        return math.sqrt(disX**2 + disY**2)

    # neighbor cost = current cost + step cost + distance(neighbor,food)
    def neighborCost(self, food, cost, dirs, head, disMap):
        neighbors = [head + neighbor for neighbor in dirs]
        count = 2
        costs = []
        for pos in neighbors:
            if disMap[pos]:
                distance = disMap[pos]
            else:
                disMap[pos] = self.distance(pos, food)
                distance = disMap[pos]
            costs.append(self.dis_weight*distance+cost+self.step_weight*2)
            # costs.append(distance+cost)
            if distance < disMap[head]:
                count -= 1

        if not count and len(dirs) == 3:
            dir = sum(dirs)
            costs[dirs.index(dir)] -= self.step_weight
        return neighbors, costs

    def find(self, food, head, tail, body, oldtail, LongestPath=0,sdf=0):
        if LongestPath:
            self.dis_weight = -self.dis_weight
            self.step_weight = -self.step_weight
        maxqsize = 0
        # ghostTrace[pos]=(pos's previous pos, the minimum cost for head to get this pos), used for dp
        ghostTrace = [None] * len(body)
        disMap = [None] * len(body)
        disMap[head] = self.distance(head, food)
        path = []

        pq = PriorityQueue()
        neighbors = [dir for dir in self.dirs if not body[head + dir]]
        neighbors, costs = self.neighborCost(food, 0, neighbors, head, disMap)

        for i in range(len(neighbors)):
            ghostTrace[neighbors[i]] = (head, costs[i])
            # print('enqueue: ', neighbors[i], "->", head, costs[i])
            pq.put(self.ghostSnake(
                neighbors[i], costs[i], head, tail, body, LongestPath))
        found = False
        while not pq.empty():   # use priority queue to find the minimum cost in all visited positions
            maxqsize = max(pq.qsize(), maxqsize)
            ghost = pq.get()
            ghosthead, cost, ghosttail, ghostbody = ghost.head, ghost.cost, ghost.tail, ghost.body
            # print('current min cost: ', ghosthead, ghostTrace[ghosthead])
            if ghosthead == food:
                if sdf:
                    found = True
                    break
                if LongestPath:
                    found = True
                    break
                stt = self.find(ghost.pretail, ghosthead, ghosttail, ghostbody, 0,1)
                if stt:
                    # print('found')
                    # print('to tail', stt)
                    # if len(stt) == 1:
                    #     print('len is 1')
                    found = True
                    # print('food:', end='')
                    break
                else:
                    # bd = body.copy()
                    # bd[tail] = 0
                    # tl = body[tail]
                    # print(body[oldtail])
                    path = self.find(oldtail, head, tail, body, 0, 1)
                    # print('not found', len(path))
                    # print('not found! GO tail', path)
                    # input()
                    # print(path)
                    return path
            neighbors = [dir for dir in self.dirs if not ghostbody[ghosthead + dir]]
            neighbors, costs = self.neighborCost(
                food, cost, neighbors, ghosthead, disMap)
            for i in range(len(neighbors)):
                if ghostTrace[neighbors[i]] and ghostTrace[neighbors[i]][1] < costs[i]:
                    continue
                ghostTrace[neighbors[i]] = (ghosthead, costs[i])
                # print('enqueue: ', neighbors[i], "->", ghosthead, costs[i])
                if neighbors[i] == food:
                    pq.put(self.ghostSnake(
                        neighbors[i], costs[i], ghosthead, ghosttail, ghostbody, LongestPath, ghost.pretail))
                else:
                    pq.put(self.ghostSnake(
                        neighbors[i], costs[i], ghosthead, ghosttail, ghostbody, LongestPath))
        if found:

            while ghosthead != head:
                path.append(ghosthead)
                ghosthead = ghostTrace[ghosthead][0]
        # print(path)
        if LongestPath:
            self.dis_weight = -self.dis_weight
            self.step_weight = -self.step_weight
        # print(maxqsize, path)
        return path
