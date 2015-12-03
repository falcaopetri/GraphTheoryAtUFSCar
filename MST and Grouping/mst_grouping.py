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
    return nx.read_gml(path, 'label')

def sum_weights(G):
    s = 0
    for edge in G.edges():
        s += G.get_edge_data(*edge)["weight"]

    return s

class MSTGrouping:
    class Criteria(Enum):
        HEAVIEST_EDGES = 1
        GROUPS_SIZE = 2

    class MST(Enum):
        PRIM = 1
        NETWORKX = 2

    def __init__(self, path):
        self.graph = read_graph(path)

    def extract_mst(self, algorithm):
        if algorithm is MSTGrouping.MST.PRIM:
            return self._extract_prim_mst()
        elif algorithm is MSTGrouping.MST.NETWORKX:
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

    def group_by(self, k, criteria, mst_method=None):
        if mst_method is None:
            mst_method = MSTGrouping.MST.PRIM
        
        T = self.extract_mst(mst_method)

        if criteria is MSTGrouping.Criteria.HEAVIEST_EDGES:
            return self._remove_with_heaviest_edges_criteria(k, T)
        
        if criteria is MSTGrouping.Criteria.GROUPS_SIZE:
            return self._remove_with_groups_size_criteria(k, T)
        
        return None

    def _remove_with_heaviest_edges_criteria(self, k, T):
        '''
            remover as k-1 maiores arestas da árvore para gerar k agrupamentos
        '''        
        remove = sorted(T.edges(), key=lambda edge: T.get_edge_data(*edge)["weight"], reverse=True)
        remove = remove[:k-1]
        T.remove_edges_from(remove)

        return T

    def _remove_with_groups_size_criteria(self, k, T):
        '''
            utilizar a medida conhecida de corte abaixo como
            critério de seleção da aresta a ser removida.
            Deve ser removida a aresta que maximiza a seguinte medida:
                w(A,B) x min{ Na, Nb }
            onde w(A,B) é o peso da aresta que liga os vértices A e B,
            Na é o número de vértices no grupo A e
            Nb é o número de vértices no grupo B
            (pois qualquer aresta removida de uma árvore gerará exatamente 2 grupos, A e B)
        '''
        while k > 1:
            self._calculate_groups_size_function(T)
            remove = sorted(T.edges(), key=lambda edge: T.get_edge_data(*edge)["group_size"],
                        reverse=True)[0]
            T.remove_edge(*remove)
            k -= 1
        return T

    def _calculate_groups_size_function(self, T):
        G = T.copy()
        for edge in T.edges():
            u, v = edge
            G.remove_edge(u, v)
            Nu = nx.node_connected_component(G, u)
            Nu = len(Nu)
            Nv = nx.node_connected_component(G, v)
            Nv = len(Nv)
            T[u][v]["group_size"] = T[u][v]["weight"] * min(Nu, Nv)
            G.add_edge(u, v)
            G[u][v] = T[u][v]
