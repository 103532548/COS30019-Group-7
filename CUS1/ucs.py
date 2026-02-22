import heapq


def ucs(origin, destinations, graph, costs):
    """
    Uniform Cost Search.

    Expands nodes in order of increasing path cost g(n).
    No heuristic is used (equivalent to A* with h(n) = 0).

    Priority queue entries:
        (g_value, node_id, insertion_counter, node_id)
    Tie-breaking (when g values are equal):
        1. Smaller node number  (ascending order rule)
        2. Earlier insertion    (chronological / FIFO order rule)

    Returns (number_of_nodes_expanded, path) or (number_of_nodes_expanded, None).
    """
    destination_set = set(destinations)

    counter = 0  # monotonically increasing insertion counter

    # heap entry: (g, node, counter, node)
    heap = [(0, origin, counter, origin)]

    g = {origin: 0}       # best known path cost to each node
    visited = set()
    parent = {origin: None}

    number_of_nodes = 0

    while heap:
        g_cur, current, _, _ = heapq.heappop(heap)

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

        # Expand neighbours in ascending node-id order so that for equal g
        # the smaller id is pushed first (and gets a lower counter too).
        for neighbour in sorted(graph[current]):
            if neighbour in visited:
                continue

            edge_cost = costs.get((current, neighbour), 1)
            tentative_g = g_cur + edge_cost

            if neighbour not in g or tentative_g < g[neighbour]:
                g[neighbour] = tentative_g
                parent[neighbour] = current
                counter += 1
                heapq.heappush(heap, (tentative_g, neighbour, counter, neighbour))

    return number_of_nodes, None  # no path found
