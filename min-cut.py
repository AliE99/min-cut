from __future__ import print_function
from __future__ import division

import random
import math
import copy
from collections import Counter
from datetime import datetime



class Graph(object):
    def __init__(self, vlist):
        self.verts = {v[0]: Counter(v[1:]) for v in vlist}
        self.update_edges()

    def update_edges(self):
        self.edges = []

        for k, v in self.verts.items():
            self.edges += ([(k, t) for t in v.keys() for n in range(v[t]) if k < t])

    @property
    def vertexCount(self):
        return len(self.verts)

    @property
    def edgeCount(self):
        return len(self.edges)

    def merge_vertices(self, edge_index):
        hi, ti = self.edges[edge_index]

        head = self.verts[hi]
        tail = self.verts[ti]

        # Remove the edge between head and tail
        del head[ti]
        del tail[hi]

        # Merge tails
        head.update(tail)

        # Update all the neighboring vertices of the fused vertex
        for i in tail.keys():
            v = self.verts[i]
            v[hi] += v[ti]
            del v[ti]

        # Finally remove the tail vertex
        del self.verts[ti]

        self.update_edges()



def contract(graph, min_v=2):
    g = copy.deepcopy(graph)
    while g.vertexCount > min_v:
        r = random.randrange(0, g.edgeCount)
        g.merge_vertices(r)

    return g



def minCut(graph):
    edge = graph.edgeCount
    vertex = graph.vertexCount
    for i in range(int(vertex * (vertex - 1) * math.log(vertex) / 2)):
        random.seed(datetime.now())
        g = contract(graph)
        edge = min(edge, g.edgeCount)
    return edge



def fastMinCut(graph):
    if graph.vertexCount <= 6:
        return minCut(graph)
    else:
        t = math.floor(1 + graph.vertexCount / math.sqrt(2))
        g1 = contract(graph, t)
        g2 = contract(graph, t)

        return min(fastMinCut(g1), fastMinCut(g2))



def findMinimum(graph):
    edge = graph.edgeCount
    vertex = graph.vertexCount
    for i in range(int(vertex * math.log(vertex) / (vertex - 1))):
        random.seed(datetime.now())
        edge = min(edge, fastMinCut(graph))
    return edge



graph = Graph([[1, 2, 3, 4], [2, 1, 3, 4], [3, 1, 2, 4], [4, 2, 3, 1]])
print("minimum cut(s) = " + str(findMinimum(graph)))
