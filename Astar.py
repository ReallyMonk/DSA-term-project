#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-04-09 20:37:07
@LastEditTime: 2020-04-10 14:27:42
'''
from queue import PriorityQueue
import math


class Astar:
    class ghostSnake:       # at every branch, send a ghost snake to all its neighbor blocks
        def __init__(self, head, weight, prehead, tail, body):
            self.head = head
            self.weight = weight
            self.body = body.copy()
            self.body[head] = prehead
            self.tail, self.body[tail] = body[tail], 0

        def __lt__(self, other):    # less than, used in prioritu queue
            return self.weight < other.weight

    def __init__(self, block_num):  # based on block_num, setup some hyperparameters
        self.dis_weight = 1         # different weight factors has different behavior
        self.step_weight = 1        # step_weigth=0 --> greedy, dis_weight=0 --> bfs
        self.bn2 = block_num+2      
        self.dirs = [-self.bn2, self.bn2, -1, +1]   # directions

    def distance(self, A, B):       # computate distance for int A and int B (one dim to two dims)
        disX, disY = A % self.bn2 - \
            B % self.bn2, A//self.bn2-B//self.bn2
        return math.sqrt(disX**2 + disY**2)


    # neighbor weight = current weight + step weight + distance(neighbor,food)
    def neighborWeight(self, food, weight, neighbors):      
        return [weight+self.distance(neighbor, food)*self.dis_weight+self.step_weight for neighbor in neighbors]


    def find(self, food, head, tail, body):
        # ghostTrace[pos]=(pos's previous pos, the minimum weight for head to get this pos), used for dp
        ghostTrace = [None] * len(body)
        pq = PriorityQueue()
        neighbors = [head + dir for dir in self.dirs if not body[head + dir]]
        weights = self.neighborWeight(food, 0, neighbors)
        for i in range(len(neighbors)):
            ghostTrace[neighbors[i]] = (head, weights[i])
            print('enqueue: ', neighbors[i], "->", head, weights[i])
            pq.put(self.ghostSnake(neighbors[i], weights[i], head, tail, body))

        found = False
        while not pq.empty():   # use priority queue to find the minimum weight in all visited positions
            ghost = pq.get()
            ghosthead = ghost.head
            print('current min weight: ', ghosthead, ghostTrace[ghosthead])
            if ghosthead == food:
                print('found')
                found = True
                break
            weight, tail, body = ghost.weight, ghost.tail, ghost.body
            neighbors = [
                ghosthead + dir for dir in self.dirs if not body[ghosthead + dir]]
            weights = self.neighborWeight(food, weight, neighbors)
            for i in range(len(neighbors)):
                if ghostTrace[neighbors[i]] and ghostTrace[neighbors[i]][1] < weights[i]:
                    continue
                ghostTrace[neighbors[i]] = (ghosthead, weights[i])
                print('enqueue: ',neighbors[i], "->", ghosthead, weights[i])
                pq.put(self.ghostSnake(
                    neighbors[i], weights[i], ghosthead, tail, body))

        path = []
        if found:
            while ghosthead != head:
                path.append(ghosthead)
                ghosthead = ghostTrace[ghosthead][0]
        path.reverse()
        print(path)
        print('here')
        return path

