def parse_file(file_path):
    Nodes = {}
    Edges = {}   # adjacency list: node -> [neighbours]
    Costs = {}   # edge costs:     (start, end) -> cost
    Origin = None
    Destinations = []

    mode = None

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line == "Nodes:":
                mode = "nodes"
                continue
            elif line == "Edges:":
                mode = "edges"
                continue
            elif line == "Origin:":
                mode = "origin"
                continue
            elif line == "Destinations:":
                mode = "destinations"
                continue

            if mode == "nodes":
                node, coordinate = line.split(":")
                node = int(node)
                coordinate = coordinate.strip("() ")
                x, y = map(int, coordinate.split(","))
                Nodes[node] = (x, y)
                Edges[node] = []
            elif mode == "edges":
                edge, cost = line.split(":")
                edge = edge.strip("()")
                start, end = map(int, edge.split(","))
                cost = int(cost.strip())
                Edges[start].append(end)
                Costs[(start, end)] = cost
            elif mode == "origin":
                Origin = int(line)
            elif mode == "destinations":
                Destinations = list(map(int, line.split(";")))

    return Nodes, Edges, Costs, Origin, Destinations
