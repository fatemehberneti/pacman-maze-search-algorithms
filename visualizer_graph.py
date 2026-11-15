import pygame
import sys
import random
from my_queue import Queue

# Constants
GRID_SIZE = 25
ROWS, COLS = 20, 20
WIDTH, HEIGHT = COLS * GRID_SIZE, ROWS * GRID_SIZE
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)      # Final path
RED = (220, 40, 40)      # Goal
BLUE = (70, 130, 230)    # Explored nodes
YELLOW = (255, 215, 0)   # Start

start = (0, 0)
goal = (ROWS - 1, COLS - 1)


def generate_maze(rows, cols):
    """Generate a cycle-free maze using randomized Prim's Algorithm."""
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

    # Ensure goal is open and connected
    goal_x, goal_y = goal
    maze[goal_x][goal_y] = 0
    if all(
        maze[goal_x + dx][goal_y + dy] == 1
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
        if 0 <= goal_x + dx < rows and 0 <= goal_y + dy < cols
    ):
        maze[goal_x - 1][goal_y] = 0

    return maze


def reconstruct_path(parent, goal_pos):
    path = []
    current = goal_pos
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path


def bfs(start_pos, goal_pos, maze):
    queue = Queue()
    queue.enqueue(start_pos)
    visited = {start_pos}
    explored_order = []
    parent = {start_pos: None}

    while not queue.is_empty():
        x, y = queue.dequeue()
        explored_order.append((x, y))
        if (x, y) == goal_pos:
            return reconstruct_path(parent, goal_pos), explored_order

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.enqueue((nx, ny))
                parent[(nx, ny)] = (x, y)

    return [], explored_order


def dfs(start_pos, goal_pos, maze):
    stack = [start_pos]
    visited = {start_pos}
    explored_order = []
    parent = {start_pos: None}

    while stack:
        x, y = stack.pop()
        explored_order.append((x, y))
        if (x, y) == goal_pos:
            return reconstruct_path(parent, goal_pos), explored_order

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                stack.append((nx, ny))
                parent[(nx, ny)] = (x, y)

    return [], explored_order


def ids(start_pos, goal_pos, maze):
    explored_order = []

    def dls(node, depth, parent, visited):
        explored_order.append(node)
        if depth == 0 and node == goal_pos:
            return True
        if depth > 0:
            x, y = node
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    if dls((nx, ny), depth - 1, parent, visited):
                        return True
        return False

    for depth in range(ROWS * COLS):
        visited = {start_pos}
        parent = {start_pos: None}
        if dls(start_pos, depth, parent, visited):
            return reconstruct_path(parent, goal_pos), explored_order

    return [], explored_order


def draw_maze(screen, maze):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if maze[row][col] == 0 else BLACK
            pygame.draw.rect(screen, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def draw_agent(screen, position, color, is_circle=False):
    if is_circle:
        x = position[1] * GRID_SIZE + GRID_SIZE // 2
        y = position[0] * GRID_SIZE + GRID_SIZE // 2
        pygame.draw.circle(screen, color, (x, y), GRID_SIZE // 2 - 2)
    else:
        pygame.draw.rect(screen, color, (position[1] * GRID_SIZE, position[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def main():
    maze = generate_maze(ROWS, COLS)

    final_path_bfs, _ = bfs(start, goal, maze)
    final_path_ids, _ = ids(start, goal, maze)
    final_path, explored_order = dfs(start, goal, maze)

    print("BFS path length:", len(final_path_bfs))
    print("IDS path length:", len(final_path_ids))
    print("DFS path length:", len(final_path))

    if not final_path:
        print("No path found from start to goal!")
        return

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Graph Search Maze Pathfinding Visualization")
    clock = pygame.time.Clock()

    explored_idx = 0
    path_idx = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        draw_maze(screen, maze)

        for pos in explored_order[:explored_idx]:
            draw_agent(screen, pos, BLUE)

        if explored_idx < len(explored_order):
            explored_idx += 1
        else:
            for pos in final_path[:path_idx]:
                draw_agent(screen, pos, GREEN)
            if path_idx < len(final_path):
                path_idx += 1

        draw_agent(screen, start, YELLOW, is_circle=True)
        draw_agent(screen, goal, RED, is_circle=True)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()