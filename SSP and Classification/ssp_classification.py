# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# TODO: documentation

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from heapq import heappush, heappop, heapify

def plot(g, i, label):
    plt.figure(i)
    edge_labels= dict([ ((u,v,), d['weight']) for u, v, d in g.edges(data=True)])

    pos = nx.circular_layout(g)
    nx.draw_networkx_nodes(g, pos=pos)
    nx.draw_networkx_edges(g, pos=pos)
    nx.draw_networkx_edge_labels(g, pos=pos, edge_labels=edge_labels, 
                                    label_pos=0.6)
    nx.draw_networkx_labels(g, pos=pos)

def read_graph(path):
    return nx.read_gml(path, 'label')

class SSPClassification:
    def __init__(self, path):
        self.graph = read_graph(path)

    def extract_ssp(self, sources, k=0):

        if len(sources) == 1 and len(sources[0]) == 0:
            sources = random.sample(self.graph.nodes(), k)
        
        return self._extract_ssp_dijkstra(sources)

    def _extract_ssp_dijkstra(self, sources):
        G = self.graph.copy()

        for node in G.nodes():
            G.node[node]["lambda"] = np.Infinity
            G.node[node]["pi"] = None

        for source in sources:
            G.node[source]["lambda"] = 0

        Q = [ (G.node[node]["lambda"], node) for node in G.nodes() ]
        heapify(Q)

        visited = []

        while len(Q) > 0:
            weight, u = heappop(Q)
            visited.append(u)

            for v in G.neighbors(u):
                if v not in visited:
                    if G.node[v]["lambda"] > G.get_edge_data(u, v)["weight"] + G.node[u]["lambda"]:
                        G.node[v]["pi"] = u
                        G.node[v]["lambda"] = G.get_edge_data(u, v)["weight"] + G.node[u]["lambda"]
                        heappush(Q, (G.node[v]["lambda"], v))

        T = nx.Graph()
        for u in G.nodes():
            T.add_node(u)

            v = G.node[u]["pi"]
            if v is not None:
                T.add_edge(u, v)
                T[u][v]["weight"] = G[u][v]["weight"]

        return T
