import heapq
from server.shared.constants import NEIGHBORS


def astar(map_manager, start, goal):
    sx, sy, sz = start
    gx, gy, gz = goal

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}

    def heuristic(a, b):
        ax, ay, az = a
        bx, by, bz = b
        # 3D Manhattan distance
        return abs(ax - bx) + abs(ay - by) + abs(az - bz)

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return list(reversed(path))

        x, y, z = current

        for dx, dy, dz in NEIGHBORS:
            nx, ny, nz = x + dx, y + dy, z + dz

            # skip blocked blocks
            cost = map_manager.get_cost(nx, ny, nz)
            if cost is None:
                continue

            # diagonal movement costs slightly more
            if dx != 0 and dz != 0:
                step_cost = 1.4 * cost
            else:
                step_cost = cost

            tentative_g = g_score[current] + step_cost

            neighbor = (nx, ny, nz)

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, neighbor))

    return None  # no path found
