# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# TODO: documentation

import argparse
from functools import partial
from time import process_time
import random_walk


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("dataset", help="Path to graph dataset (.gml format)")
    parser.add_argument("method", help="Method to use", choices=["steady", "power", "random"])
    parser.add_argument("-n", "--iterations", type=int, help="Number of iterations to run. Default: 5", default=5)
    parser.add_argument("-f", "--frequent", type=int, help="Number most frequent to show. Default: 10", default=10)
    parser.add_argument("-v", "--verbose", action='store_true', help="Show all vertices value")
    parser.add_argument("-t", "--timeit", action='store_true', help="Print execution time of chosen method")
    parser.add_argument("-p", "--plot", action='store_true', help="Plot the graph")
    
    args = parser.parse_args()
    
    walk = random_walk.RandomWalk(args.dataset)

    if (args.plot):
        walk.plot()
    
    result = None
    fn = None
    if (args.method == "steady"):
        print("Steady method:")
        fn = partial(walk.steady_state)
    elif (args.method == "power"):
        print("Power method with %d iterations:" % args.iterations)
        fn = partial(walk.power_method, args.iterations)
    elif (args.method == "random"):
        print("Random Walk method with %d iterations:" % args.iterations)
        fn = partial(walk.random_walk, args.iterations)

    
    t = process_time()
    result = fn()
    elapsed_time = process_time() - t
    
    if (args.timeit):
        print("Time: %.5f seconds" % elapsed_time)
    
    if (args.verbose):
        print("Result matrix:")
        print(result)
    
    most = random_walk.get_most_frequent(args.frequent, result)
    print("Top %d most frequent:" % args.frequent)
    for x, y in most.items():
        print("%d %.5f" % (x, y))
    

if __name__ == "__main__":
    main()
