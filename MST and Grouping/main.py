# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# TODO: documentation

import argparse
from functools import partial
from time import process_time
import mst_grouping
import matplotlib.pyplot as plt
import networkx as nx

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("dataset", help="Path to graph dataset (.gml format)")
    parser.add_argument("criteria", help="Criteria to use on grouping", choices=["heaviest", "size"])
    parser.add_argument("-k", "--kgroups", type=int, help="Number groups to generate", required=True)
    parser.add_argument("-v", "--verbose", action='store_true', help="Show all vertices value")
    parser.add_argument("-t", "--timeit", action='store_true', help="Print execution time of chosen method")
    parser.add_argument("-p", "--plot", action='store_true', help="Plot the graphs generated")

    args = parser.parse_args()

    graph = mst_grouping.MSTGrouping(args.dataset)

    fn = None
    if (args.criteria == "heaviest"):
        print("Generating %d groups using greatest criteria:" % args.kgroups)
        fn = partial(graph.group_by, args.kgroups, mst_grouping.MSTGrouping.Criteria.HEAVIEST_EDGES)
    elif (args.criteria == "size"):
        print("Generating %d groups using group size criteria:" % args.kgroups)
        fn = partial(graph.group_by, args.kgroups, mst_grouping.MSTGrouping.Criteria.GROUPS_SIZE)

    t = process_time()
    grouped_graph = fn()
    elapsed_time = process_time() - t

    if (args.timeit):
        print("Time: %.5f seconds" % elapsed_time)

    print("Groups formed:")
    for x in nx.connected_components(grouped_graph):
        print(x)

    if (args.verbose):
        mst_nx = graph.extract_mst(mst_grouping.MSTGrouping.MST.NETWORKX)
        mst_prim = graph.extract_mst(mst_grouping.MSTGrouping.MST.PRIM)
        sum_nx = mst_grouping.sum_weights(mst_nx)
        sum_prim = mst_grouping.sum_weights(mst_prim)

        print("MST weight sum compare:")
        print(" - NetworkX (Kruskal): %d" % sum_nx)
        print(" - Prim              : %d" % sum_prim)

    if (args.plot):
        mst_grouping.plot(graph.graph, 1, "Graph")
        mst_grouping.plot(graph.extract_mst(mst_grouping.MSTGrouping.MST.NETWORKX), 2, "MST Graph")
        mst_grouping.plot(grouped_graph, 3, "Grouped Graph")
        plt.show()

if __name__ == "__main__":
    main()
