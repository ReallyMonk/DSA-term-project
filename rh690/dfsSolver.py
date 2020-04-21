import random


class bfsSolver():
    def __init__(self):
        # print('create solver')
        pass

    def update_info(self, head, tail, body, food, width):
        self.head = head
        self.tail = tail
        self.body = body
        self.food = food
        self.width = width
        self.walls = []
        self.set_walls()

    def set_walls(self):
        w = self.width
        self.walls.extend(range(w))
        self.walls.extend(range((w - 1) * w, w * w))

        for i in range(1, w - 1):
            self.walls.append(i * w)
            self.walls.append((i + 1) * w - 1)
        return

    def connect(self, a):
        # the map is store in 1-D array
        # so the connected nodes can be decided by index
        # if the other nodes is not wall
        # then nodes n is connected to
        # node n-1, n+1, n-width, n+width
        w = self.width
        walls = self.walls
        connect_node = []
        _map = self.body
        if a - 1 not in walls and _map[a - 1] == 0:
            connect_node.append(a - 1)

        if a + 1 not in walls and _map[a + 1] == 0:
            connect_node.append(a + 1)

        if a + w not in walls and _map[a + w] == 0:
            connect_node.append(a + w)

        if a - w not in walls and _map[a - w] == 0:
            connect_node.append(a - w)

        return connect_node

    def bfs(self, head, end):
        path = [None for i in range(self.width**2)]
        path[head] = head
        queue = [head]

        while queue and not path[end]:
            tmp = []
            tmp.extend(queue)
            for node in tmp:
                # print('current node: ', node)
                # print('cur queue ', queue)
                con_nodes = self.connect(node)

                # add new node in to the queue
                # set the last node in path
                for new_node in con_nodes:
                    if not path[new_node]:
                        queue.append(new_node)
                        path[new_node] = node

                # pop out queue
                queue.remove(node)
                # print('cur que ', queue)

        #print('out')
        #print('food', self.food, ' head ', self.head)
        if not path[end]:
            return False
        else:
            s_path = []
            pre = end
            while head != pre:
                s_path.append(pre)
                pre = path[pre]

            # s_path.append(pre)
            # print(s_path)
        return s_path

    def find_path(self):
        # a stratgy to enhance the program
        # if snake can reach the food, go for it
        # if snkae can not reach the food, trace the tail
        # if not, go where every you can
        r_path = self.bfs(self.head, self.food)

        if r_path:
            pass
        else:
            tail_nbr = self.connect(self.tail)
            if tail_nbr:
                for nbr in tail_nbr:
                    r_path = self.bfs(self.head, nbr)
                    if r_path:
                        break
                    else:
                        dirs = self.connect(self.head)
                        #print(dirs)
                        if not dirs:
                            r_path = []
                        else:
                            seed = random.randint(0, len(dirs)-1)
                            r_path = [dirs[seed]]
        
        return r_path

    '''
        if not r_path:
            return []
        else:
            # path = [i for i in reversed(r_path)]
            # return false means try to go where every snake can
       ''' 

        

