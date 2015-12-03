# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# TODO: documentation

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from heapq import heappush, heappop, heapify

def plot(g, i, title):
    fig = plt.figure(i)
    fig.canvas.set_window_title(title) 
    edge_labels= dict([ ((u,v,), d['weight']) for u, v, d in g.edges(data=True)])

    pos = nx.circular_layout(g)
    nx.draw_networkx_nodes(g, pos=pos)
    nx.draw_networkx_edges(g, pos=pos)
    nx.draw_networkx_edge_labels(g, pos=pos, edge_labels=edge_labels, 
                                    label_pos=0.6)
    nx.draw_networkx_labels(g, pos=pos)

def read_graph(path):
    if path.endswith('.txt'):
        A = np.loadtxt(path)
        
        G = nx.from_numpy_matrix(A)
        return G

    if path.endswith('.gml'):
        A = nx.read_gml(path, 'label')
        return nx.read_gml(path, 'label')

def sum_weights(G):
    s = 0
    for edge in G.edges():
        s += G.get_edge_data(*edge)["weight"]

    return s

class TSP:
    class MST(Enum):
        PRIM = 1
        NETWORKX = 2

    def __init__(self, path):
        self.graph = read_graph(path)

    def extract_mst(self, algorithm):
        if algorithm is TSP.MST.PRIM:
            return self._extract_prim_mst()
        elif algorithm is TSP.MST.NETWORKX:
            return nx.prim_mst(self.graph)

    def _extract_prim_mst(self):
        G = self.graph.copy()

        for node in G.nodes():
            G.node[node]["lambda"] = np.Infinity
            G.node[node]["pi"] = None

        first = G.nodes()[0]
        G.node[first]["lambda"] = 0

        Q = [ (G.node[node]["lambda"], node) for node in G.nodes() ]
        heapify(Q)

        visited = []

        while len(Q) > 0:
            weight, u = heappop(Q)
            visited.append(u)

            for v in G.neighbors(u):
                if v not in visited:
                    if G.node[v]["lambda"] > G.get_edge_data(u, v)["weight"]:
                        G.node[v]["pi"] = u
                        G.node[v]["lambda"] = G.get_edge_data(u, v)["weight"]
                        heappush(Q, (G.node[v]["lambda"], v))

        T = nx.Graph()
        for u in G.nodes():
            T.add_node(u)

            v = G.node[u]["pi"]
            if v is not None:
                T.add_edge(u, v)
                T[u][v]["weight"] = G[u][v]["weight"]

        return T

    def twice_around(self, source=None):
        if source is None:
            source = np.random.choice(self.graph.nodes())

        T = self.extract_mst(TSP.MST.PRIM)
        T = nx.MultiGraph(T)

        T.add_edges_from(T.edges(data=True))
        
        eulerian_circuit = nx.eulerian_circuit(T, source)

        visited = []
        hamiltonian_path = []

        for u,v in eulerian_circuit:
            if u not in visited:
                visited.append(u)
                hamiltonian_path.append(u)

        hamiltonian_path.append(hamiltonian_path[0])

        hamiltonian_graph = nx.create_empty_copy(self.graph)

        for i in range(len(hamiltonian_path)-1):
            edge = (hamiltonian_path[i], hamiltonian_path[i+1])
            hamiltonian_graph.add_edge(*edge, self.graph.get_edge_data(*edge))
            
        return (hamiltonian_graph, hamiltonian_path)
