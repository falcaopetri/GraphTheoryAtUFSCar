# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# TODO: documentation

import argparse
from functools import partial
from time import process_time
import ssp_classification
import matplotlib.pyplot as plt
import networkx as nx

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("dataset", help="Path to graph dataset (.gml format)")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-k", "--kgroups", type=int, help="Number of groups to generate. Random Sources")
    group.add_argument("-s", "--sources", help="Shortest Path sources. Comma separeted. Ex: Brighton,Edinburgh", default="")
    
    parser.add_argument("-v", "--verbose", action='store_true', help="Show all vertices value")
    parser.add_argument("-t", "--timeit", action='store_true', help="Print execution time of chosen method")
    parser.add_argument("-p", "--plot", action='store_true', help="Plot the graphs generated")

    args = parser.parse_args()
    args.sources = args.sources.split(",")

    graph = ssp_classification.SSPClassification(args.dataset)
    
    t = process_time()
    grouped_graph = graph.extract_ssp(args.sources, args.kgroups)
    elapsed_time = process_time() - t

    if (args.timeit):
        print("Time: %.5f seconds" % elapsed_time)

    print("Groups formed:")
    for x in nx.connected_components(grouped_graph):
        print(x)

    if (args.plot):
        ssp_classification.plot(graph.graph, 1, "Graph")
        ssp_classification.plot(grouped_graph, 2, "Grouped Graph")
        plt.show()

if __name__ == "__main__":
    main()
