# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# TODO: documentation

import argparse
from functools import partial
from time import process_time
import tsp
import matplotlib.pyplot as plt
import networkx as nx

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("dataset", help="Path to graph dataset (.gml format)")
    parser.add_argument("-n", "--number", type=int, help="Number of solutions to generate", required=True)
    parser.add_argument("-v", "--verbose", action='store_true', help="Show all vertices value")
    parser.add_argument("-t", "--timeit", action='store_true', help="Print execution time of chosen method")
    parser.add_argument("-p", "--plot", action='store_true', help="Plot the graphs generated")

    args = parser.parse_args()

    graph = tsp.TSP(args.dataset)

    if (args.plot):
        tsp.plot(graph.graph, 0, "Graph")

    for i in range(args.number):
        t = process_time()
        (hamiltonian_graph, hamiltonian_path) = graph.twice_around()
        elapsed_time = process_time() - t

        print("TSP solution #%d: %d" % (i+1, tsp.sum_weights(hamiltonian_graph)))
        if args.verbose:
            print("Path: ", end="")
            for j in range(len(hamiltonian_path)):
                if j != 0: print(" -> ", end="")

                print(hamiltonian_path[j], end="")
            print()

        if (args.timeit):
            print("Time: %.5f seconds" % elapsed_time)

        if (args.plot):
            tsp.plot(hamiltonian_graph, i+1, "Hamiltonian Graph #" + str(i+1))

        print()
    if args.plot:
        plt.show()

if __name__ == "__main__":
    main()
