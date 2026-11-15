import random
from collections import deque

ROWS, COLS = 20, 20
start = (0, 0)
goal = (ROWS - 1, COLS - 1)


def generate_maze(rows, cols):
    """Generate a maze using Prim's Algorithm."""
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
    return maze


def bfs_node(start_pos, goal_pos, maze):
    queue = deque([start_pos])
    visited = {start_pos}
    nodes_explored = 0

    while queue:
        x, y = queue.popleft()
        nodes_explored += 1
        if (x, y) == goal_pos:
            return nodes_explored

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))

    return nodes_explored


def dfs_node(start_pos, goal_pos, maze):
    stack = [start_pos]
    visited = {start_pos}
    nodes_explored = 0

    while stack:
        x, y = stack.pop()
        nodes_explored += 1
        if (x, y) == goal_pos:
            return nodes_explored

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                stack.append((nx, ny))

    return nodes_explored


def ids_node(start_pos, goal_pos, maze):
    def dls(node, depth, visited, nodes_explored):
        if depth == 0 and node == goal_pos:
            return True, nodes_explored
        if depth > 0:
            x, y = node
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    nodes_explored += 1
                    found, nodes_explored = dls((nx, ny), depth - 1, visited, nodes_explored)
                    if found:
                        return True, nodes_explored
        return False, nodes_explored

    nodes_explored = 0
    for depth in range(ROWS * COLS):
        visited = {start_pos}
        found, nodes_explored = dls(start_pos, depth, visited, nodes_explored)
        if found:
            return nodes_explored

    return nodes_explored


def bfs_time(start_pos, goal_pos, maze):
    queue = deque([start_pos])
    visited = {start_pos}

    while queue:
        x, y = queue.popleft()
        if (x, y) == goal_pos:
            return True

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))

    return False


def dfs_time(start_pos, goal_pos, maze):
    stack = [start_pos]
    visited = {start_pos}

    while stack:
        x, y = stack.pop()
        if (x, y) == goal_pos:
            return True

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                stack.append((nx, ny))

    return False


def ids_time(start_pos, goal_pos, maze):
    def dls(node, depth, visited):
        if depth == 0 and node == goal_pos:
            return True
        if depth > 0:
            x, y = node
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    if dls((nx, ny), depth - 1, visited):
                        return True
        return False

    for depth in range(ROWS * COLS):
        visited = {start_pos}
        if dls(start_pos, depth, visited):
            return True

    return False