# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# TODO: documentation

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import operator
from collections import OrderedDict


def read_graph(path):
    return nx.read_gml(path)

def get_most_frequent(n, lst):
    d = {}

    for i in range(len(lst)):
        d[i] = lst[i]
    
    return OrderedDict(sorted(d.items(), key=operator.itemgetter(1), reverse=True)[0:n])


class RandomWalk:
    def __init__(self, path):
        self.graph = read_graph(path)
        
    def plot(self):
        nx.draw(self.graph)
        plt.show()

    def steady_state(self):
        steady = []
        g = self.graph
        
        number_of_edges = nx.number_of_edges(g)
        for key, item in g.degree().items():
            steady.append(item / (2 * number_of_edges ))
        
        return steady

    def power_method(self, n):
        sum_degree = sum(self.graph.degree().values())
        number_of_nodes = nx.number_of_nodes(self.graph)
        
        w = [1/number_of_nodes  for x in range(number_of_nodes)]
        
        probability_matrix = self.probability_matrix()
        prob_to_the_nth = probability_matrix ** n
        
        return np.array(np.dot(w, prob_to_the_nth))[0]

    def probability_matrix(self):
        delta = np.diag([1/d for d in self.graph.degree().values()])
        delta = np.asmatrix(delta)
        
        adjacency = nx.to_numpy_matrix(self.graph)
        
        return np.dot(delta, adjacency)

    def random_walk(self, n):
        visited = [0] * self.graph.number_of_nodes()
        
        curr_node = np.random.choice(self.graph.nodes())
        visited[curr_node] += 1

        for i in range(n):
            neighbors = self.graph.neighbors(curr_node)
            curr_node = np.random.choice(neighbors)
            visited[curr_node] += 1
            
        random = [i/n for i in visited]
        return random
