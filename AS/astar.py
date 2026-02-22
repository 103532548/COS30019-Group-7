import heapq
import math


def euclidean(coord1, coord2):
    """Straight-line distance between two (x, y) coordinate pairs."""
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)


def heuristic(node, destinations, nodes):
    """
    Minimum Euclidean distance from *node* to any destination.
    This is h(n) — admissible because straight-line distance never
    overestimates the true cost.
    """
    return min(euclidean(nodes[node], nodes[d]) for d in destinations)


def astar(origin, destinations, graph, costs, nodes):
    """
    A* Search.

    f(n) = g(n) + h(n)
        g(n) – actual cost accumulated from origin to n
        h(n) – Euclidean distance from n to the nearest destination

    Priority queue entries:
        (f_value, node_id, insertion_counter, node_id)
    Tie-breaking (when f values are equal):
        1. Smaller node number  (ascending order rule)
        2. Earlier insertion    (chronological / FIFO order rule)

    Returns (number_of_nodes_expanded, path) or (number_of_nodes_expanded, None).
    """
    destination_set = set(destinations)

    h_start = heuristic(origin, destinations, nodes)
    counter = 0  # monotonically increasing insertion counter

    # heap entry: (f, node, counter, node)
    heap = [(h_start, origin, counter, origin)]

    g = {origin: 0}          # best known g-cost to each node
    visited = set()
    parent = {origin: None}

    number_of_nodes = 0

    while heap:
        f, current, _, _ = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)
        number_of_nodes += 1  # count each node when it is *expanded*

        if current in destination_set:
            # Reconstruct path
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            return number_of_nodes, path

        # Expand neighbours in ascending node-id order so that for equal f
        # the smaller id is pushed first (gets a lower counter too).
        for neighbour in sorted(graph[current]):
            if neighbour in visited:
                continue

            edge_cost = costs.get((current, neighbour), 1)
            tentative_g = g[current] + edge_cost

            if neighbour not in g or tentative_g < g[neighbour]:
                g[neighbour] = tentative_g
                parent[neighbour] = current
                h_n = heuristic(neighbour, destinations, nodes)
                f_n = tentative_g + h_n
                counter += 1
                heapq.heappush(heap, (f_n, neighbour, counter, neighbour))

    return number_of_nodes, None  # no path found
