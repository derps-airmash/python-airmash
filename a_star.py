
import heapq


def reconstruct_path(route, current):
    path = [current]
    while current in route:
        current = route[current]
        path.append(current)
    return path[::-1]


def astar(start, goal, neighbours, cost_estimate):
    # For each node, which node it can most efficiently be reached from. If a
    # node can be reached from many nodes, route will eventually contain
    # the most efficient previous step.
    route = {}

    # For each node, the cost of getting from the start node to that node.
    gScore = {
        # The cost of going from start to start is zero.
        start: 0.0,
    }

    # For each node, the total cost of getting from the start node to the goal
    # by passing by that node. That value is partly known, partly heuristic.
    fScore = {
        # For the first node, that value is completely heuristic.
        start: cost_estimate(start, goal)
    }

    # The set of nodes already evaluated
    visited = set()

    # The set of currently discovered nodes that are not evaluated yet.
    # Initially, only the start node is known.
    to_visit = [(0.0, start)]
    to_visit_set = set([start])

    while to_visit:
        #  the node in openSet having the lowest fScore[] value
        _, current = heapq.heappop(to_visit)
        visited.add(current)

        if current == goal:
            return {
                'visited': len(visited),
                'path': reconstruct_path(route, current),
            }

        for neighbour in neighbours(current):
            if neighbour in visited:
                continue  # Ignore the neighbour which is already evaluated.

            # The distance from start to a neighbour
            tentative_gScore = gScore[current] + 1.0
            if neighbour not in fScore:
                fScore[neighbour] = tentative_gScore + cost_estimate(neighbour, goal)

            if neighbour not in to_visit_set:  # Discover a new node
                heapq.heappush(to_visit, (fScore[neighbour], neighbour))
                to_visit_set.add(neighbour)
            elif neighbour in gScore and tentative_gScore >= gScore[neighbour]:
                continue  # This is not a better path.

            # This path is the best until now. Record it!
            route[neighbour] = current
            gScore[neighbour] = tentative_gScore
