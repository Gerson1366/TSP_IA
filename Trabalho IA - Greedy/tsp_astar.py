from argparse import ArgumentParser
import os.path
from datetime import datetime
from graph import Graph

import heapq


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def empty(self):
        return len(self.queue) == 0

    def put(self, item, priority):
        heapq.heappush(self.queue, (priority, item))

    def get(self):
        return heapq.heappop(self.queue)[1]


def heuristic(a, b):
    # Manhattan distance on a square grid
    return abs(int(a) - int(b)) + abs(int(a) - int(b))


class Node:
    def __init__(self, node, h=None, g=None, f=None):
        self.node = node
        self.h = h
        self.g = g
        self.f = f

    def __repr__(self):
        return self.node


class AStar:

    def __init__(self, start, graph):
        self.start = start
        self.graph = graph

    def lowest_cost(self, origin, neighbors):
        h = float('Inf')
        g = 0
        f = h + g
        nearest = None

        for neighbour in neighbors:
            if neighbour == origin.node:
                continue
            nh = heuristic(origin.node, neighbour)
            ng = (origin.g or 0) + self.graph.cost(origin.node, neighbour)
            nf = nh + ng
            if nf < f:
                h = nh
                g = ng
                f = nf
                nearest = neighbour

        return Node(nearest, h, g, f)

    def run(self):
        missing = list(self.graph.vertices())  # towns to be visited
        route = []

        current = Node(self.start)
        route.append(current.node)
        missing.remove(current.node)

        while len(missing) > 0:
            current = self.lowest_cost(current, missing)
            route.append(current.node)
            missing.remove(current.node)  # remove visited town

            # going back to start city
            if current.node is not self.start and len(missing) == 0:
                missing.append(self.start)

        return route, current.g


def tsp_astar():
    help_description = "The program accepts the path of .JSON file as input and computes the path using Genethic algorithm"
    parserArg = ArgumentParser(description=help_description)
    parserArg.add_argument("-file", help="TSP File Path", required=True)
    args = parserArg.parse_args()
    f_name = args.file
    if(f_name=="brazil58"):
        graph = Graph('data/brazil58.json')
    elif(f_name=="eil101"):
        graph = Graph('data/eil101.json')
    elif(f_name=="gil262"):
        graph = Graph('data/gil262.json')
    else:
        print('Escolha um arquivo valido')  
    start_time = datetime.now()
    came_from, cost_so_far = AStar('0', graph).run()
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print("Elapsed Time:", str(elapsed_time), "ms")
    print("Cost:", cost_so_far)
    print("Path:", came_from)

tsp_astar()
