## Random Walks

### Execução
```
walks.py dataset {steady,power,random} [-n ITERATIONS] [-f FREQUENT] [-v] [-t] [-p]
```
#### Argumentos

positional arguments:
  - `dataset`

    Path to graph dataset (.gml format)
  - `{steady,power,random}`

    Method to use

optional arguments:
  - `-h`, `--help`

    show this help message and exit

  - `-n ITERATIONS`, `--iterations ITERATIONS`

    Number of iterations to run. Default: 5

  - `-f FREQUENT`, `--frequent FREQUENT`

    Number most frequent to show. Default: 10
  - `-v`, `--verbose`

    Show all vertices value
  - `-t`, `--timeit`

    Print execution time of chosen method
  - `-p`, `--plot`

    Plot the graph
