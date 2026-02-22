import sys
from parser import parse_file
from ucs import ucs


def main():
    filename = sys.argv[1]
    method = sys.argv[2]

    nodes, edges, costs, origin, destinations = parse_file(filename)

    if filename is None:
        print("No file provided")
        exit()

    if method == "CUS1":
        number_of_nodes, path = ucs(origin, destinations, edges, costs)
    else:
        print("No method implemented")
        exit()

    if number_of_nodes and path is not None:
        print(filename, method)
        print(path[-1], number_of_nodes)  # last element = goal node
        print(" ".join(map(str, path)))
    else:
        print(filename, method)
        print("Search failed")


if __name__ == "__main__":
    main()
