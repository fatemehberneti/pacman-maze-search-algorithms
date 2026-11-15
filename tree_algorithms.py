from collections import deque
import random
import heapq

ROWS, COLS = 10, 10
start = (0, 0)
goal = (ROWS - 1, COLS - 1)


class TreeNode:
    def __init__(self, position, path):
        self.position = position
        self.path = path


def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    walls = []
    start_x, start_y = start
    maze[start_x][start_y] = 0

    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = start_x + dx, start_y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            walls.append((nx, ny))

    while walls:
        wall_x, wall_y = random.choice(walls)
        walls.remove((wall_x, wall_y))
        neighbors = []

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = wall_x + dx, wall_y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                neighbors.append((nx, ny))

        if len(neighbors) == 1:
            maze[wall_x][wall_y] = 0
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = wall_x + dx, wall_y + dy
                if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 1:
                    walls.append((nx, ny))

    goal_x, goal_y = goal
    maze[goal_x][goal_y] = 0
    # Guarantee at least one open neighbor next to the goal so it is never sealed off
    if maze[goal_x - 1][goal_y] == 1 and maze[goal_x][goal_y - 1] == 1:
        maze[goal_x - 1][goal_y] = 0

    return maze


def bfs_tree(start_pos, goal_pos, maze):
    queue = deque([TreeNode(start_pos, [start_pos])])
    nodes_explored = 0

    while queue:
        node = queue.popleft()
        nodes_explored += 1

        if node.position == goal_pos:
            return node.path, nodes_explored

        x, y = node.position
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0 and (nx, ny) not in node.path:
                queue.append(TreeNode((nx, ny), node.path + [(nx, ny)]))

    return [], nodes_explored


def dfs_tree(start_pos, goal_pos, maze):
    stack = [TreeNode(start_pos, [start_pos])]
    nodes_explored = 0

    while stack:
        node = stack.pop()
        nodes_explored += 1

        if node.position == goal_pos:
            return node.path, nodes_explored

        x, y = node.position
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0 and (nx, ny) not in node.path:
                stack.append(TreeNode((nx, ny), node.path + [(nx, ny)]))

    return [], nodes_explored


def ids_tree(start_pos, goal_pos, maze):
    nodes_explored = 0

    def dls(node, depth, path):
        nonlocal nodes_explored
        if depth == 0 and node == goal_pos:
            return path
        if depth > 0:
            x, y = node
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0 and (nx, ny) not in path:
                    nodes_explored += 1
                    found_path = dls((nx, ny), depth - 1, path + [(nx, ny)])
                    if found_path:
                        return found_path
        return None

    for depth in range(ROWS * 3):
        found_path = dls(start_pos, depth, [start_pos])
        if found_path:
            return found_path, nodes_explored
    return [], nodes_explored


def a_star_tree_manhattan(start_pos, goal_pos, maze):
    def manhattan_heuristic(current, target):
        return abs(current[0] - target[0]) + abs(current[1] - target[1])

    open_list = []
    heapq.heappush(open_list, (0, start_pos, [start_pos]))
    g_cost = {start_pos: 0}
    nodes_explored = 0

    while open_list:
        _, current_position, path = heapq.heappop(open_list)
        nodes_explored += 1

        if current_position == goal_pos:
            return path, nodes_explored

        x, y = current_position
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0:
                new_g_cost = g_cost[current_position] + 1
                if neighbor not in g_cost or new_g_cost < g_cost[neighbor]:
                    g_cost[neighbor] = new_g_cost
                    f_cost = new_g_cost + manhattan_heuristic(neighbor, goal_pos)
                    heapq.heappush(open_list, (f_cost, neighbor, path + [neighbor]))

    return [], nodes_explored


def a_star_tree_euclidean(start_pos, goal_pos, maze):
    def euclidean_heuristic(current, target):
        return ((current[0] - target[0]) ** 2 + (current[1] - target[1]) ** 2) ** 0.5

    open_list = []
    heapq.heappush(open_list, (0, start_pos, [start_pos]))
    g_cost = {start_pos: 0}
    nodes_explored = 0

    while open_list:
        _, current_position, path = heapq.heappop(open_list)
        nodes_explored += 1

        if current_position == goal_pos:
            return path, nodes_explored

        x, y = current_position
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0:
                new_g_cost = g_cost[current_position] + 1
                if neighbor not in g_cost or new_g_cost < g_cost[neighbor]:
                    g_cost[neighbor] = new_g_cost
                    f_cost = new_g_cost + euclidean_heuristic(neighbor, goal_pos)
                    heapq.heappush(open_list, (f_cost, neighbor, path + [neighbor]))

    return [], nodes_explored