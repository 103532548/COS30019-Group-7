import heapq
import math


def euclidean(coord1, coord2):
    """Straight-line distance between two (x, y) coordinate pairs."""
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)


def heuristic(node, destinations, nodes):
    """
    Minimum Euclidean distance from *node* to any destination node.
    This is the greedy heuristic h(n).
    """
    return min(euclidean(nodes[node], nodes[d]) for d in destinations)


def gbfs(origin, destinations, graph, nodes):
    """
    Greedy Best-First Search.

    Priority queue entries are tuples:
        (h_value, node_id, insertion_counter, node_id)
    where:
        h_value           – heuristic distance to nearest goal
        node_id           – used as secondary tie-breaker (ascending order)
        insertion_counter – tertiary tie-breaker (chronological / FIFO order)

    Returns (number_of_nodes_expanded, path) or (number_of_nodes_expanded, None).
    """
    destination_set = set(destinations)

    h_start = heuristic(origin, destinations, nodes)
    counter = 0  # monotonically increasing insertion counter
    # heap entry: (h, node, counter, node)  — node appears twice so heapq
    # never needs to compare the parent dictionary (non-comparable).
    heap = [(h_start, origin, counter, origin)]
    visited = set()
    parent = {origin: None}

    number_of_nodes = 0

    while heap:
        h, current, _, _ = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)
        number_of_nodes += 1  # count each node when it is *expanded*

        if current in destination_set:
            # Reconstruct path from origin to current
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            return number_of_nodes, path

        # Expand neighbours in ascending node-id order so that when two
        # neighbours share the same h value the smaller id is pushed first
        # and therefore gets a smaller counter — satisfying both tie-breaking
        # rules simultaneously.
        for neighbour in sorted(graph[current]):
            if neighbour not in visited:
                if neighbour not in parent:
                    parent[neighbour] = current
                counter += 1
                h_n = heuristic(neighbour, destinations, nodes)
                heapq.heappush(heap, (h_n, neighbour, counter, neighbour))

    return number_of_nodes, None  # no path found
