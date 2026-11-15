import pygame
import sys
from collections import deque
import random
import heapq

# Constants
GRID_SIZE = 45
ROWS, COLS = 10, 10
WIDTH, HEIGHT = COLS * GRID_SIZE, ROWS * GRID_SIZE
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (220, 40, 40)
BLUE = (70, 130, 230)
ORANGE = (255, 165, 0)

start = (0, 0)
goal = (ROWS - 1, COLS - 1)


class TreeNode:
    def __init__(self, position, path):
        self.position = position
        self.path = path


def generate_maze(rows, cols, wall_probability=0.25):
    maze = []
    for _ in range(rows):
        row = [1 if random.random() < wall_probability else 0 for _ in range(cols)]
        maze.append(row)
    maze[start[0]][start[1]] = 0
    maze[goal[0]][goal[1]] = 0
    return maze


def bfs_tree(start_pos, goal_pos, maze):
    queue = deque([TreeNode(start_pos, [start_pos])])
    steps = []

    while queue:
        node = queue.popleft()
        steps.append((node.position, False))

        if node.position == goal_pos:
            for pos in node.path:
                steps.append((pos, True))
            return steps

        x, y = node.position
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0 and (nx, ny) not in node.path:
                queue.append(TreeNode((nx, ny), node.path + [(nx, ny)]))

    return steps


def dfs_tree(start_pos, goal_pos, maze):
    stack = [TreeNode(start_pos, [start_pos])]
    steps = []

    while stack:
        node = stack.pop()
        steps.append((node.position, False))

        if node.position == goal_pos:
            for pos in node.path:
                steps.append((pos, True))
            return steps

        x, y = node.position
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0 and (nx, ny) not in node.path:
                stack.append(TreeNode((nx, ny), node.path + [(nx, ny)]))

    return steps


def ids_tree(start_pos, goal_pos, maze):
    def dls(node, depth):
        steps = []
        if node.position == goal_pos:
            for pos in node.path:
                steps.append((pos, True))
            return steps, True

        if depth == 0:
            steps.append((node.position, False))
            return steps, False

        steps.append((node.position, False))
        x, y = node.position
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0 and (nx, ny) not in node.path:
                result, found = dls(TreeNode((nx, ny), node.path + [(nx, ny)]), depth - 1)
                steps.extend(result)
                if found:
                    return steps, True
        return steps, False

    for depth in range(ROWS * COLS):
        steps, found = dls(TreeNode(start_pos, [start_pos]), depth)
        if found:
            return steps
    return []


def a_star_tree_manhattan(start_pos, goal_pos, maze):
    def manhattan_heuristic(current, target):
        return abs(current[0] - target[0]) + abs(current[1] - target[1])

    open_list = []
    heapq.heappush(open_list, (0, start_pos, [start_pos]))
    g_cost = {start_pos: 0}
    steps = []

    while open_list:
        _, current_position, path = heapq.heappop(open_list)
        steps.append((current_position, False))

        if current_position == goal_pos:
            for pos in path:
                steps.append((pos, True))
            return steps

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

    return steps


def a_star_tree_euclidean(start_pos, goal_pos, maze):
    def euclidean_heuristic(current, target):
        return ((current[0] - target[0]) ** 2 + (current[1] - target[1]) ** 2) ** 0.5

    open_list = []
    heapq.heappush(open_list, (0, start_pos, [start_pos]))
    g_cost = {start_pos: 0}
    steps = []

    while open_list:
        _, current_position, path = heapq.heappop(open_list)
        steps.append((current_position, False))

        if current_position == goal_pos:
            for pos in path:
                steps.append((pos, True))
            return steps

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

    return steps


def draw_maze(screen, maze):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if maze[row][col] == 0 else BLACK
            pygame.draw.rect(screen, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, (220, 220, 220), (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)


def draw_agent(screen, position, color, is_circle=False):
    if is_circle:
        x = position[1] * GRID_SIZE + GRID_SIZE // 2
        y = position[0] * GRID_SIZE + GRID_SIZE // 2
        pygame.draw.circle(screen, color, (x, y), GRID_SIZE // 3)
    else:
        pygame.draw.rect(screen, color, (position[1] * GRID_SIZE, position[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def main():
    maze = generate_maze(ROWS, COLS)
    algorithms = [
        ("BFS Tree Search", bfs_tree),
        ("DFS Tree Search", dfs_tree),
        ("IDS Tree Search", ids_tree),
        ("A* (Manhattan)", a_star_tree_manhattan),
        ("A* (Euclidean)", a_star_tree_euclidean),
    ]

    results = []
    for name, func in algorithms:
        steps = func(start, goal, maze)
        explored = [pos for pos, final in steps if not final]
        final_path = [pos for pos, final in steps if final]
        print(f"--- {name} ---")
        print(f"Explored nodes count: {len(explored)} | Final path length: {len(final_path)}")
        results.append((name, steps))

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    for name, steps in results:
        pygame.display.set_caption(f"Maze Search Visualization — {name}")
        if not steps:
            continue

        step_index = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(BLACK)
            draw_maze(screen, maze)

            explored_positions = set()
            final_path_positions = set()

            for i in range(step_index + 1):
                pos, is_final_path = steps[i]
                if is_final_path:
                    final_path_positions.add(pos)
                else:
                    explored_positions.add(pos)

            for pos in explored_positions:
                draw_agent(screen, pos, BLUE)
            for pos in final_path_positions:
                draw_agent(screen, pos, ORANGE, is_circle=True)

            draw_agent(screen, start, GREEN)
            draw_agent(screen, goal, RED)

            pygame.display.flip()
            clock.tick(FPS)

            if step_index < len(steps) - 1:
                step_index += 1
            else:
                break

        pygame.time.wait(1000)

    pygame.quit()


if __name__ == "__main__":
    main()